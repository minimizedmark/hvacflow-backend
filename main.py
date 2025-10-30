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
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HVACFlow.app</title>
        <style>
            body { background:#000; color:#0f0; font-family:Arial; margin:0; padding:20px; }
            h1 { margin:0 0 20px; }
            #chat { height:70vh; overflow:auto; border:1px solid #0f0; padding:10px; background:#111; border-radius:8px; }
            #input { width:100%; padding:12px; background:#111; color:#0f0; border:1px solid #0f0; margin-top:10px; border-radius:8px; font-size:16px; }
            p { margin:8px 0; }
        </style>
    </head>
    <body>
      <h1>HVACFlow™</h1>
      <div id="chat"></div>
      <input id="input" placeholder="AC not cooling?" />
      <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');

        async function ask(q) {
          try {
            const res = await fetch('/ask', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ q })
            });
            const data = await res.json();
            return data.reply || "No response";
          } catch (e) {
            return "Error: " + e.message;
          }
        }

        input.onkeypress = async (e) => {
          if (e.key === 'Enter' && input.value.trim()) {
            const msg = input.value.trim();
            chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
            input.value = '';
            chat.innerHTML += `<p><i>Thinking...</i></p>`;
            chat.scrollTop = chat.scrollHeight;

            const reply = await ask(msg);
            const thinking = chat.querySelector('p:last-child');
            if (thinking && thinking.innerText.includes('Thinking')) {
              thinking.outerHTML = `<p><b>HVACFlow™:</b> ${reply}</p>`;
            } else {
              chat.innerHTML += `<p><b>HVACFlow™:</b> ${reply}</p>`;
            }
            chat.scrollTop = chat.scrollHeight;
          }
        };
      </script>
    </body>
    </html>
    """

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    q = data.get("q", "").strip()
    if not q:
        return {"reply": "Please type a message."}

    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(
                "https://api.x.ai/v1/chat/completions",
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "You are HVACFlow™. Diagnose HVAC issues. Be helpful. End with: Ready to book? Reply ZIP."},
                        {"role": "user", "content": q}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=30.0
            )
            r.raise_for_status()
            response_data = r.json()
            if "choices" in response_data and response_data["choices"]:
                return {"reply": response_data["choices"][0]["message"]["content"]}
            else:
                return {"reply": "No response from Grok. Try again."}
        except httpx.HTTPStatusError as e:
            return {"reply": f"API Error {e.response.status_code}"}
        except Exception as e:
            return {"reply": "Service error. Try refreshing."}
