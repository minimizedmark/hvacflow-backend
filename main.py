from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # ← ADD THIS
import httpx
import os

app = FastAPI()

# ADD CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
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
    <head><title>HVACFlow.app</title></head>
    <body style="background:#000;color:#0f0;font-family:Arial;margin:0;padding:20px;">
      <h1>HVACFlow™</h1>
      <div id="chat" style="height:70vh;overflow:auto;border:1px solid #0f0;padding:10px;background:#111;"></div>
      <input id="input" placeholder="AC not cooling?" style="width:100%;padding:12px;background:#111;color:#0f0;border:1px solid #0f0;margin-top:10px;" />
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
            return "Network error: " + e.message;
          }
        }

        input.onkeypress = async (e) => {
          if (e.key === 'Enter' && input.value.trim()) {
            const msg = input.value.trim();
            chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
            input.value = '';
            chat.innerHTML += `<p><i>Thinking...</i></p>`;
            const reply = await ask(msg);
            chat.innerHTML = chat.innerHTML.replace('<p><i>Thinking...</i></p>', `<p><b>HVACFlow™:</b> ${reply}</p>`);
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
                    "temperature": 0.7
                },
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=30.0
            )
            r.raise_for_status()
            response_data = r.json()
            if "choices" in response_data and response_data["choices"]:
                return {"reply": response_data["choices"][0]["message"]["content"]}
            else:
                return {"reply": "Grok didn't respond. Try again."}
        except httpx.HTTPStatusError as e:
            return {"reply": f"API Error {e.response.status_code}: {e.response.text[:100]}"}
        except Exception as e:
            return {"reply": "Service error. Try refreshing."}
