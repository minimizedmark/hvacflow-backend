from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

GROK_API = "https://api.x.ai/v1/chat/completions"
API_KEY = os.getenv("API_KEY")  # ← GETS FROM RENDER

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <body style="background:#000;color:#0f0;font-family:Arial;text-align:center;padding:50px;">
      <h1>HVACFlow™ Live</h1>
      <a href="/demo" style="color:#0f0;font-size:20px;">Open Chat Demo →</a>
    </body>
    """

@app.get("/demo", response_class=HTMLResponse)
async def demo():
    with open("demo.html") as f:
        return f.read()

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    q = data.get("q", "")
    async with httpx.AsyncClient() as client:
        r = await client.post(GROK_API, json={
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": "You are HVACFlow™. Diagnose, book, be helpful. End with: Ready to book? Reply ZIP."},
                {"role": "user", "content": q}
            ],
            "temperature": 0.7
        }, headers={"Authorization": f"Bearer {API_KEY}"})
        reply = r.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
