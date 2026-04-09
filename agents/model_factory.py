from agno.models.google import Gemini
from agno.models.groq import Groq
import Calibrazione


def get_model(model_id=None, temperature=None):
    """
    Ritorna un'istanza del modello basata sulle impostazioni in Calibrazione.py.

    Per i modelli Qwen 3 su Groq, disabilita il thinking mode (chain-of-thought
    visibile in inglese) tramite il parametro API `enable_thinking=False`.
    """
    provider = Calibrazione.LLM_PROVIDER.lower()

    if provider == "qwen":
        model_name = model_id or Calibrazione.MODEL_TECH_SPECIALISTS
        # Per i modelli Qwen 3 su Groq, il thinking mode è controllato da
        # Calibrazione.QWEN_THINKING_ENABLED. Se disabilitato, passa
        # enable_thinking=False all'API per eliminare il preamble in inglese.
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
        model_name = model_id or Calibrazione.MODEL_TECH_SPECIALISTS
        return Gemini(id=model_name, api_key=Calibrazione.GEMINI_API_KEY, temperature=temperature)

    else:
        raise ValueError(f"Provider LLM '{provider}' non supportato.")
