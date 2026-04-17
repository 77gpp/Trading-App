#!/usr/bin/env python3
"""Test Gemma 4 context window support (128k tokens)"""

import sys
from agents.model_factory import get_model

def test_gemma_context():
    """Test if Gemma 4 supports 128k context window"""

    print("🧪 Testing Gemma 4 context window...")
    print("-" * 60)

    # Get Gemma 4 model
    try:
        model = get_model()
        print(f"✅ Model loaded: {type(model).__name__}")
        print(f"   ID: {model.id if hasattr(model, 'id') else 'N/A'}")
        print(f"   Base URL: {model.base_url if hasattr(model, 'base_url') else 'N/A'}")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

    # Create a large prompt (~50k tokens to test if 128k works)
    # Each repetition adds ~300 tokens
    dummy_text = "This is a test sentence to fill the context window. " * 3000
    test_prompt = f"""You are a concise assistant. Answer briefly.

Context (large test data - {len(dummy_text)} characters):
{dummy_text}

Question: What is the maximum context window size you support? Answer in one sentence."""

    print(f"\n📊 Prompt size: ~{len(test_prompt) // 4} tokens (rough estimate)")
    print("\n⏳ Sending request to Gemma 4...")

    try:
        # Simple message
        response = model.response(test_prompt)
        print(f"\n✅ Request successful!")
        print(f"Response: {response}\n")
        return True
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Request failed: {error_msg}\n")

        # Check if it's a context size error
        if "exceed_context_size" in error_msg or "exceeds the available context" in error_msg:
            print("⚠️  Context window exceeded! Gemma 4 may not be configured to 128k.")
            return False
        elif "timed out" in error_msg.lower():
            print("⚠️  Request timed out (possible server issue).")
            return False
        else:
            return False

if __name__ == "__main__":
    success = test_gemma_context()
    sys.exit(0 if success else 1)
