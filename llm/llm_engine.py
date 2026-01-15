"""LLM Engine using OpenRouter API"""

import os
import requests
from typing import Optional, List, Dict

class LLMEngine:
    """Interface to OpenRouter API for LLM calls"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "mistral-7b"):
        """
        Initialize LLM Engine
        
        Args:
            api_key: OpenRouter API key (or use OPENROUTER_API_KEY env var)
            model: Model to use (mistral-7b, mixtral-8x7b, neural-chat-7b, llama-2-7b)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY env var or pass api_key parameter")
        
        # Map friendly names to OpenRouter model IDs (using :free suffix for free tier)
        self.model_map = {
            "mistral-7b": "mistralai/mistral-7b-instruct:free",
        }
        
        self.model = self.model_map.get(model, model)  # Support both friendly names and full model IDs
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate text using LLM
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0=deterministic, 1=creative)
            
        Returns:
            Generated text response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "Error: No response from model"
                
        except requests.exceptions.RequestException as e:
            return f"Error calling OpenRouter API: {str(e)}"
    
    def list_available_models(self) -> Dict[str, str]:
        """List available model aliases"""
        return self.model_map
    
    def test_connection(self) -> bool:
        """Test if API key is valid"""
        try:
            response = self.generate("Hi", max_tokens=10)
            return "Error" not in response
        except Exception:
            return False
