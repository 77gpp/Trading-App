#!/usr/bin/env python3
"""Test Gemma 4 context window directly via OpenAI API"""

import sys
from openai import OpenAI

def test_gemma_context():
    """Test if Gemma 4 supports 128k context window"""

    print("🧪 Testing Gemma 4 context window (direct OpenAI API)...")
    print("-" * 60)

    # Initialize OpenAI client with Gemma 4 endpoint
    client = OpenAI(
        api_key="not-needed",
        base_url="http://localhost:8080/v1"
    )

    # Create a large prompt (~50k tokens to test if 128k works)
    dummy_text = "This is a test sentence to fill the context window. " * 3000

    messages = [
        {
            "role": "user",
            "content": f"""You are a concise assistant. Answer briefly.

Context (large test data - {len(dummy_text)} characters):
{dummy_text}

Question: What is the maximum context window size you support? Answer in one sentence."""
        }
    ]

    prompt_tokens_estimate = len(dummy_text) // 4 + 50
    print(f"📊 Message size: ~{prompt_tokens_estimate:,} tokens (rough estimate)")
    print("⏳ Sending request to Gemma 4...")

    try:
        response = client.chat.completions.create(
            model="gemma4",
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )

        print(f"\n✅ Request successful!")
        print(f"\nResponse: {response.choices[0].message.content}\n")

        # Check usage if available
        if hasattr(response, 'usage'):
            print(f"📊 Token usage:")
            print(f"   Input tokens: {response.usage.prompt_tokens:,}")
            print(f"   Output tokens: {response.usage.completion_tokens:,}")

        return True

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Request failed:")
        print(f"   {error_msg}\n")

        # Check if it's a context size error
        if "exceed_context_size" in error_msg or "exceeds the available context" in error_msg:
            print("⚠️  Context window exceeded! Gemma 4 is NOT configured to 128k.")
            print("    Current context window appears to be less than 50k tokens.")
            return False
        elif "Connection" in error_msg or "refused" in error_msg:
            print("⚠️  Cannot connect to Gemma 4 server at http://localhost:8080")
            print("    Is the server running?")
            return False
        else:
            return False

if __name__ == "__main__":
    success = test_gemma_context()
    sys.exit(0 if success else 1)
