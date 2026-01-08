import streamlit as st
from groq import Groq
def get_groq_client() -> Groq:
    """
    Create and return Groq client using Streamlit secrets.
    """
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Please add it to .streamlit/secrets.toml"
        )

    return Groq(api_key=api_key)
def call_llm(prompt: str) -> str:
    """
    Send prompt to Groq LLM and return generated text.
    """
    try:
        client = get_groq_client()

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical decision-support assistant."
                },
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
        return (
            "LLM_ERROR: AI service temporarily unavailable. "
            f"Details: {str(e)}"
        )
