"""Confidence Scoring based on Retrieval Relevance"""

from typing import List, Dict, Any
import statistics


class ConfidenceScorer:
    """Calculate confidence scores for RAG responses"""
    
    # Confidence thresholds
    HIGH_CONFIDENCE = 0.7
    MEDIUM_CONFIDENCE = 0.5
    LOW_CONFIDENCE = 0.3
    
    @staticmethod
    def calculate_relevance_score(distances: List[float]) -> float:
        """
        Calculate overall relevance score from distance metrics
        
        Args:
            distances: List of distance scores from vector search
            
        Returns:
            Relevance score (0-1, higher is better)
        """
        if not distances:
            return 0.0
        
        # Convert distances to similarities (1 - distance)
        similarities = [1 - d for d in distances]
        
        # Calculate average similarity
        avg_similarity = statistics.mean(similarities)
        
        return avg_similarity
    
    @staticmethod
    def calculate_confidence(distances: List[float], 
                           num_results: int,
                           min_expected_results: int = 3) -> Dict[str, Any]:
        """
        Calculate confidence score and level
        
        Args:
            distances: Distance scores from search
            num_results: Number of results returned
            min_expected_results: Minimum expected results for high confidence
            
        Returns:
            Dict with confidence score, level, and reasoning
        """
        if not distances:
            return {
                "score": 0.0,
                "level": "NONE",
                "reasoning": "No relevant documents found"
            }
        
        # Calculate relevance score
        relevance_score = ConfidenceScorer.calculate_relevance_score(distances)
        
        # Adjust based on number of results
        result_penalty = 1.0
        if num_results < min_expected_results:
            result_penalty = num_results / min_expected_results
        
        # Final confidence score
        confidence_score = relevance_score * result_penalty
        
        # Determine confidence level
        if confidence_score >= ConfidenceScorer.HIGH_CONFIDENCE:
            level = "HIGH"
            reasoning = "Multiple highly relevant documents found"
        elif confidence_score >= ConfidenceScorer.MEDIUM_CONFIDENCE:
            level = "MEDIUM"
            reasoning = "Relevant documents found with moderate similarity"
        elif confidence_score >= ConfidenceScorer.LOW_CONFIDENCE:
            level = "LOW"
            reasoning = "Limited relevant information available"
        else:
            level = "VERY LOW"
            reasoning = "Weak relevance to query"
        
        return {
            "score": round(confidence_score, 3),
            "level": level,
            "reasoning": reasoning,
            "details": {
                "avg_relevance": round(relevance_score, 3),
                "num_results": num_results,
                "top_relevance": round(1 - distances[0], 3) if distances else 0.0
            }
        }
    
    @staticmethod
    def add_confidence_disclaimer(answer: str, confidence_level: str) -> str:
        """
        Add appropriate disclaimer based on confidence level
        
        Args:
            answer: Generated answer
            confidence_level: Confidence level (HIGH/MEDIUM/LOW/VERY LOW)
            
        Returns:
            Answer with disclaimer if needed
        """
        if confidence_level == "VERY LOW" or confidence_level == "LOW":
            disclaimer = "\n\n⚠️ Note: This answer has limited supporting evidence in the available documents. Please verify with additional sources."
            return answer + disclaimer
        elif confidence_level == "MEDIUM":
            disclaimer = "\n\nℹ️ Note: This answer is based on available documents but may not be complete."
            return answer + disclaimer
        else:
            # HIGH confidence - no disclaimer needed
            return answer
    
    @staticmethod
    def calculate_source_scores(distances: List[float], 
                               metadatas: List[Dict]) -> List[Dict[str, Any]]:
        """
        Calculate individual source scores with metadata
        
        Args:
            distances: Distance scores
            metadatas: Metadata for each source
            
        Returns:
            List of source scores with details
        """
        source_scores = []
        
        for i, (dist, meta) in enumerate(zip(distances, metadatas), 1):
            relevance = 1 - dist
            
            # Determine quality label
            if relevance >= 0.7:
                quality = "Highly Relevant"
            elif relevance >= 0.5:
                quality = "Moderately Relevant"
            elif relevance >= 0.3:
                quality = "Somewhat Relevant"
            else:
                quality = "Weakly Relevant"
            
            source_scores.append({
                "rank": i,
                "source": meta.get("source_document", "Unknown"),
                "section": meta.get("section_title", "N/A"),
                "relevance_score": round(relevance, 3),
                "relevance_percent": f"{relevance * 100:.1f}%",
                "quality": quality
            })
        
        return source_scores
