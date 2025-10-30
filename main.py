from xai import Grok
import os

client = Grok(api_key=os.getenv("XAI_API_KEY"))

def hvac_chatbot(user_query: str, user_history: str = "") -> str:
    system_prompt = f"""
    You are HVAC Helper: Witty, pro tech. Diagnose AC/furnace woes.
    Safe DIY tips only. Upsell bookings gently.
    History: {user_history}
    """.strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    payload = {
        "model": "grok-4",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.7
        # ZERO extras. No stream. No name. Nada.
    }

    try:
        response = client.chat.completions.create(**payload)
        return response.choices[0].message.content
    except Exception as e:
        return f"Grok glitch: {str(e)} — blame the API, not me this time."
