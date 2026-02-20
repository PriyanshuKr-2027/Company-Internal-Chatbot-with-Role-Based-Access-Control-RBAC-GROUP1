"""Prompt Templates and Context Augmentation for RAG"""

from typing import List, Dict, Any


class PromptTemplates:
    """Centralized prompt templates for different query types"""
    
    # System prompt for RAG responses
    SYSTEM_PROMPT = """You are an AI assistant for a company internal chatbot system.
Your role is to provide accurate, helpful answers based ONLY on the company documents provided.

Key Guidelines:
- Answer questions using only the information from the provided documents
- If information is not in the documents, clearly state "I don't have that information in the available documents"
- Be concise and professional
- Cite sources when making specific claims
- If documents are contradictory, acknowledge this
- Do not make up or infer information not present in the documents
"""

    @staticmethod
    def format_context(documents: List[str], metadatas: List[Dict], distances: List[float]) -> str:
        """
        Format search results into context for LLM
        
        Args:
            documents: List of document chunks
            metadatas: List of metadata dicts
            distances: List of distance scores
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
            source = meta.get("source_document", "Unknown")
            section = meta.get("section_title", "N/A")
            relevance = (1 - dist) * 100
            
            context_parts.append(
                f"[Source {i}: {source} - {section}] (Relevance: {relevance:.1f}%)\n{doc}"
            )
        
        return "\n\n".join(context_parts)
    
    @staticmethod
    def build_rag_prompt(query: str, context: str, include_citations: bool = True) -> str:
        """
        Build complete RAG prompt with query and context
        
        Args:
            query: User's question
            context: Formatted context from documents
            include_citations: Whether to request citations
            
        Returns:
            Complete prompt for LLM
        """
        citation_instruction = ""
        if include_citations:
            citation_instruction = "\nWhen referencing specific information, cite the source number (e.g., [Source 1])."
        
        prompt = f"""{PromptTemplates.SYSTEM_PROMPT}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Answer the question based on the context documents above
- Be clear, concise, and professional
- If the answer is not in the documents, say so{citation_instruction}

ANSWER:"""
        
        return prompt
    
    @staticmethod
    def build_comparison_prompt(query: str, context: str) -> str:
        """
        Build prompt for comparison queries
        
        Args:
            query: Comparison question
            context: Formatted context
            
        Returns:
            Prompt optimized for comparisons
        """
        prompt = f"""{PromptTemplates.SYSTEM_PROMPT}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Compare the relevant information from the documents
- Present key similarities and differences
- Use a structured format (bullet points or table if appropriate)
- Cite sources for each point

COMPARISON:"""
        
        return prompt
    
    @staticmethod
    def build_summary_prompt(query: str, context: str) -> str:
        """
        Build prompt for summary/overview queries
        
        Args:
            query: Summary question
            context: Formatted context
            
        Returns:
            Prompt optimized for summaries
        """
        prompt = f"""{PromptTemplates.SYSTEM_PROMPT}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Provide a comprehensive summary of the relevant information
- Organize information logically
- Highlight key points
- Include important details from the documents

SUMMARY:"""
        
        return prompt
    
    @staticmethod
    def build_factual_prompt(query: str, context: str) -> str:
        """
        Build prompt for factual/specific queries
        
        Args:
            query: Factual question
            context: Formatted context
            
        Returns:
            Prompt optimized for factual answers
        """
        prompt = f"""{PromptTemplates.SYSTEM_PROMPT}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {query}

INSTRUCTIONS:
- Provide a direct, factual answer
- Include specific numbers, dates, or names if present
- Cite the source of the information
- Keep the answer focused and precise

ANSWER:"""
        
        return prompt
    
    @staticmethod
    def detect_query_type(query: str) -> str:
        """
        Detect the type of query to select appropriate template
        
        Args:
            query: User question
            
        Returns:
            Query type: 'comparison', 'summary', 'factual', or 'general'
        """
        query_lower = query.lower()
        
        # Comparison indicators
        comparison_words = ['compare', 'difference', 'versus', 'vs', 'contrast', 'better', 'worse']
        if any(word in query_lower for word in comparison_words):
            return 'comparison'
        
        # Summary indicators
        summary_words = ['summarize', 'overview', 'summary', 'explain', 'describe', 'what are all']
        if any(word in query_lower for word in summary_words):
            return 'summary'
        
        # Factual indicators (specific questions)
        factual_words = ['when', 'where', 'who', 'how many', 'how much', 'what is the']
        if any(word in query_lower for word in factual_words):
            return 'factual'
        
        return 'general'
    
    @staticmethod
    def get_prompt_for_query(query: str, context: str, include_citations: bool = True) -> str:
        """
        Get the most appropriate prompt based on query type
        
        Args:
            query: User question
            context: Formatted context
            include_citations: Whether to include citations
            
        Returns:
            Optimized prompt for the query type
        """
        query_type = PromptTemplates.detect_query_type(query)
        
        if query_type == 'comparison':
            return PromptTemplates.build_comparison_prompt(query, context)
        elif query_type == 'summary':
            return PromptTemplates.build_summary_prompt(query, context)
        elif query_type == 'factual':
            return PromptTemplates.build_factual_prompt(query, context)
        else:
            return PromptTemplates.build_rag_prompt(query, context, include_citations)
