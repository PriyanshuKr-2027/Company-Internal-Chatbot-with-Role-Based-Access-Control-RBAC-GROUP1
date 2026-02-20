"""Configuration for LLM Integration"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model Selection (using mistral-7b-instruct:free from OpenRouter)
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "mistral-7b")

# Model Configuration
LLM_CONFIG = {
    "max_tokens": 500,
    "temperature": 0.7,  # 0=deterministic, 1=creative
    "top_p": 0.9,
    "top_k": 40,
}

# Answer Generation Config
ANSWER_GENERATION_CONFIG = {
    "max_tokens": 300,
    "temperature": 0.5,  # Lower for more consistent answers
}

# Re-ranking Config
RERANKING_CONFIG = {
    "max_tokens": 50,
    "temperature": 0.1,  # Very low for consistent scoring
}

# Available Models Mapping (using :free suffix for free tier)
AVAILABLE_MODELS = {
    "mistral-7b": "mistralai/mistral-7b-instruct:free",
}

# OpenRouter Endpoint (corrected to .ai domain)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Feature Flags
FEATURES = {
    "enable_llm": True,
    "enable_answer_generation": True,
    "enable_reranking": True,
    "enable_query_expansion": False,  # Future feature
}
