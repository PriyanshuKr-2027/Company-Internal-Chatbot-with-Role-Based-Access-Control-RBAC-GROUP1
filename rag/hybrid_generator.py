"""Hybrid approach: Direct extraction + minimal LLM formatting"""

from typing import Dict, Any, List
import json

from rag.prompt_templates import PromptTemplates

class HybridAnswerGenerator:
    """Generate complete answers using direct extraction + LLM enhancement"""
    
    def __init__(self, llm_engine, query_engine):
        self.llm = llm_engine
        self.query_engine = query_engine
    
    def generate_answer(self, user_query: str, documents: List[str], 
                       metadatas: List[Dict], user_role: str = "employee", 
                       is_hr_query: bool = False, is_aggregation: bool = False) -> str:
        """
        Generate complete answer using hybrid approach:
        1. Extract structured content directly from documents
        2. Use LLM only for formatting/enhancement
        
        Args:
            user_query: User question
            documents: Retrieved documents
            metadatas: Document metadata
            user_role: User's role
            is_hr_query: Whether this is an HR/employee query
            is_aggregation: True if the HR query is a count/total request
            
        Returns:
            Complete, formatted answer
        """
        
        # HR queries get structured formatting for headcount/list outputs
        if is_hr_query:
            return self._format_hr_response(
                user_query=user_query,
                documents=documents,
                metadatas=metadatas,
                is_aggregation=is_aggregation
            )
        
        # Step 1: Extract structured content directly from documents
        extracted_content = self._extract_structured_content(
            user_query, documents, metadatas
        )
        
        # If we have strong direct extraction, minimize LLM usage
        if extracted_content and len(extracted_content) > 500:
            # LLM is only used for light formatting
            formatting_prompt = f"""Please format and organize the following information clearly and comprehensively.
Keep all the content. Just organize it with proper sections, bullet points, and clear structure:

{extracted_content}

Question was: {user_query}"""
            
            formatted = self.llm.generate(
                prompt=formatting_prompt,
                max_tokens=800,
                temperature=0.3  # Lower temp for consistency
            )
            return formatted
        else:
            # Fallback: Use LLM with context for generation
            context = "\n\n".join(documents[:5])
            full_prompt = f"""Answer the following question comprehensively based on this context:

CONTEXT:
{context}

QUESTION: {user_query}

Provide a complete, detailed answer covering all aspects of the question."""
            
            return self.llm.generate(
                prompt=full_prompt,
                max_tokens=1000,
                temperature=0.5
            )
    
    def _extract_structured_content(self, query: str, documents: List[str], 
                                   metadatas: List[Dict]) -> str:
        """Extract structured information directly from documents"""
        
        query_lower = query.lower()
        extracted = []
        
        # Pattern-based extraction for common queries
        for doc, meta in zip(documents, metadatas):
            section = meta.get("section", "")
            
            # Extract bullet points and structured content
            lines = doc.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith(('*', '-', '•', '##', '###', '####')):
                    # Include bullet points and headers
                    extracted.append(line)
                elif i > 0 and lines[i-1].strip().startswith(('*', '-', '•')):
                    # Include content under bullets
                    extracted.append(line)
            
            # Add section header
            if section and extracted and not extracted[-1].startswith('#'):
                extracted.insert(len(extracted)-len([l for l in extracted if l == section]), 
                               f"\n### {section}\n")
        
        return "\n".join(extracted[:50])  # Limit to prevent huge prompts

    def _format_hr_response(self, user_query: str, documents: List[str], 
                            metadatas: List[Dict], is_aggregation: bool) -> str:
        """Format HR responses as counts or employee lists."""
        records = self._extract_hr_records(documents, metadatas)

        if is_aggregation:
            total = len(records)
            if total == 0:
                return "No matching employees found."
            dept_counts: Dict[str, int] = {}
            for rec in records:
                dept = rec.get("department", "Unknown")
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
            dept_lines = [f"- {dept}: {count}" for dept, count in sorted(dept_counts.items())]
            dept_block = "\n".join(dept_lines)
            return f"Total employees: {total}\nBy department:\n{dept_block}"

        if not records:
            return "No matching employees found."

        def sort_key(rec: Dict[str, str]):
            name = rec.get("name", "")
            parts = name.split()
            return (parts[-1] if parts else "", name)

        sorted_records = sorted(records, key=sort_key)
        lines = []
        for idx, rec in enumerate(sorted_records, 1):
            name = rec.get("name", "Unknown")
            role = rec.get("role", "Unknown")
            dept = rec.get("department", "Unknown")
            manager = rec.get("manager", None)
            base_line = f"{idx}. {name} — {role} ({dept})"
            if manager:
                base_line += f", Manager: {manager}"
            lines.append(base_line)
        lines.append(f"Total: {len(sorted_records)} employees")
        return "\n".join(lines)

    def _extract_hr_records(self, documents: List[str], metadatas: List[Dict]) -> List[Dict[str, str]]:
        """Extract minimal HR fields from metadata/text with safe fallbacks."""
        records: List[Dict[str, str]] = []
        for doc, meta in zip(documents, metadatas):
            # Try metadata first
            name = meta.get("employee_name") or meta.get("name")
            role = meta.get("employee_role") or meta.get("role")
            dept = meta.get("employee_dept") or meta.get("employee_department") or meta.get("department")
            manager = meta.get("manager_id")

            # If metadata missing, parse from document text
            if not name:
                name = self._parse_field_from_text(doc, "Full Name:")
            if not role:
                role = self._parse_field_from_text(doc, "Role:")
            if not dept:
                dept = self._parse_field_from_text(doc, "Department:")
            if not manager:
                manager = self._parse_manager_from_text(doc)

            if name or role or dept:
                records.append({
                    "name": name or "Unknown",
                    "role": role or "Unknown",
                    "department": dept or "Unknown",
                    "manager": manager
                })
        return records

    def _parse_field_from_text(self, text: str, field_label: str) -> str:
        """Parse a specific field from HR document text."""
        if field_label in text:
            # Find the line with the field
            for line in text.split("\n"):
                if field_label in line:
                    # Extract value after the label
                    value = line.split(field_label, 1)[-1].strip()
                    return value
        return ""

    def _parse_manager_from_text(self, text: str) -> str:
        """Lightweight parse for manager info inside HR text."""
        lowered = text.lower()
        markers = ["manager:", "manager id:", "reports to"]
        for marker in markers:
            if marker in lowered:
                segment = lowered.split(marker, 1)[-1]
                candidate = segment.split("\n", 1)[0].strip().strip("-: ")
                if candidate:
                    return candidate
        return ""


# Integration helper
def create_hybrid_generator(llm_engine, query_engine):
    """Factory function to create hybrid generator"""
    return HybridAnswerGenerator(llm_engine, query_engine)
