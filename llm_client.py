from groq import Groq
import streamlit as st


# =====================================================
# INITIALIZE GROQ CLIENT
# =====================================================
# Make sure GROQ_API_KEY is set in .streamlit/secrets.toml
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# =====================================================
# MAIN LLM CALL FUNCTION
# =====================================================
def call_llm(prompt: str) -> str:
    """
    Calls Groq LLM and returns generated text.

    Args:
        prompt (str): Input prompt for the LLM

    Returns:
        str: Generated response text or error message
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ Supported free model
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        # Safe fallback (important for Streamlit Cloud)
        return (
            "⚠️ LLM service temporarily unavailable.\n\n"
            f"Details: {str(e)}"
        )
