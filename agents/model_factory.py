import os
from agno.models.google import Gemini
from agno.models.groq import Groq
import settings

def get_model(model_id=None):
    """
    Ritorna un'istanza del modello basata sulle impostazioni in settings.py.
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "qwen":
        # Usiamo Groq per Qwen 2.5
        model_name = model_id or settings.MODEL_TECH_SPECIALISTS
        return Groq(id=model_name, api_key=settings.GROQ_API_KEY)
    
    elif provider == "gemini":
        # Fallback su Gemini
        model_name = model_id or settings.MODEL_TECH_SPECIALISTS
        return Gemini(id=model_name, api_key=settings.GEMINI_API_KEY)
    
    else:
        raise ValueError(f"Provider LLM '{provider}' non supportato.")
