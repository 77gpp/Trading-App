from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAILike
import Calibrazione


def get_model(model_id=None, temperature=None, agent_name=None):
    """
    Ritorna un'istanza del modello basata sulle impostazioni in Calibrazione.py.

    Supporta tre provider:
    - 'gemma4': Gemma 4 locale su http://localhost:8080 (OpenAI-compatible)
    - 'qwen': Qwen 3 su Groq via API
    - 'gemini': Google Gemini via API

    Se agent_name è fornito, legge la configurazione per-agente da AGENT_LLM_CONFIG.
    """
    if agent_name and hasattr(Calibrazione, 'AGENT_LLM_CONFIG'):
        cfg = Calibrazione.AGENT_LLM_CONFIG.get(agent_name, {})
        provider = cfg.get("provider", Calibrazione.LLM_PROVIDER).lower()
        model_id = cfg.get("model") or model_id
    else:
        provider = Calibrazione.LLM_PROVIDER.lower()

    if provider == "gemma4":
        model_name = model_id or Calibrazione.MODEL_GEMMA4
        return OpenAILike(
            id=model_name,
            api_key="not-needed",
            base_url=Calibrazione.GEMMA4_BASE_URL,
            temperature=temperature,
        )

    elif provider == "qwen":
        available_qwen = getattr(Calibrazione, 'AVAILABLE_MODELS', {}).get('qwen', ["llama-3.3-70b-versatile"])
        # Se model_id non è compatibile con Groq (es. "gemma4"), usa il primo modello Groq disponibile
        if model_id and model_id in available_qwen:
            model_name = model_id
        else:
            model_name = available_qwen[0]
        extra_params = {}
        if "qwen3" in model_name.lower() and not Calibrazione.QWEN_THINKING_ENABLED:
            extra_params["request_params"] = {"enable_thinking": False}
        return Groq(
            id=model_name,
            api_key=Calibrazione.GROQ_API_KEY,
            temperature=temperature,
            **extra_params,
        )

    elif provider == "gemini":
        available_gemini = getattr(Calibrazione, 'AVAILABLE_MODELS', {}).get('gemini', ["gemini-2.0-flash"])
        if model_id and model_id in available_gemini:
            model_name = model_id
        else:
            model_name = available_gemini[0]
        return Gemini(id=model_name, api_key=Calibrazione.GEMINI_API_KEY, temperature=temperature)

    else:
        raise ValueError(f"Provider LLM '{provider}' non supportato. Scegli tra: 'gemma4', 'qwen', 'gemini'.")
