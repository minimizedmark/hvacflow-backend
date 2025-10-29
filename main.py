from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

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
          const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ q })
          });
          const data = await res.json();
          return data.reply;
        }

        input.onkeypress = async (e) => {
          if (e.key === 'Enter' && input.value) {
            const msg = input.value;
            chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
            input.value = '';
            const reply = await ask(msg);
            chat.innerHTML += `<p><b>HVACFlow™:</b> ${reply}</p>`;
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
    q = data.get("q", "")
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
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return {"reply": response_data["choices"][0]["message"]["content"]}
            else:
                return {"reply": "Sorry, I couldn't process that. Try again."}
        except httpx.HTTPStatusError as e:
            return {"reply": f"API Error: {e.response.status_code}"}
        except Exception as e:
            return {"reply": "Service temporarily down. Try again soon."}
