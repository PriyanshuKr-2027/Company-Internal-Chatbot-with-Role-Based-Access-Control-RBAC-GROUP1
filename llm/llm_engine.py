import json
import os
import time
from typing import Optional
import requests
class LLMEngine:
    """
    Minimal OpenRouter client using the provided request format.
    Includes retry logic with exponential backoff for rate limiting.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "google/gemma-3n-e2b-it:free"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided")
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.max_retries = 3
        self.base_wait_time = 2  # Start with 2 seconds

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Company Internal Chatbot",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url=self.api_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=45,
                )
                
                # Handle 429 rate limit with exponential backoff
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        wait_time = self.base_wait_time * (2 ** attempt)
                        print(f"Rate limited (429). Retrying in {wait_time}s... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        detail = response.text
                        raise RuntimeError(f"OpenRouter error: 429 Too Many Requests | {detail}")
                
                response.raise_for_status()
                result = response.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
                raise RuntimeError("No choices returned from OpenRouter response")
                
            except requests.HTTPError as e:
                detail = response.text
                last_error = RuntimeError(f"OpenRouter error: {e} | {detail}")
                if response.status_code != 429:  # Don't retry on other errors
                    raise last_error
        
        if last_error:
            raise last_error
        raise RuntimeError("Max retries exceeded")
