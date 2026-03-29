import os
from agno.models.google import Gemini
from agno.models.groq import Groq
import Calibrazione

def get_model(model_id=None):
    """
    Ritorna un'istanza del modello basata sulle impostazioni in Calibrazione.py.
    """
    provider = Calibrazione.LLM_PROVIDER.lower()
    
    if provider == "qwen":
        # Usiamo Groq per Qwen 2.5
        model_name = model_id or Calibrazione.MODEL_TECH_SPECIALISTS
        return Groq(id=model_name, api_key=Calibrazione.GROQ_API_KEY)
    
    elif provider == "gemini":
        # Fallback su Gemini
        model_name = model_id or Calibrazione.MODEL_TECH_SPECIALISTS
        return Gemini(id=model_name, api_key=Calibrazione.GEMINI_API_KEY)
    
    else:
        raise ValueError(f"Provider LLM '{provider}' non supportato.")
