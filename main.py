from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

GROK_API = "https://api.x.ai/v1/chat/completions"
API_KEY = "YOUR_XAI_KEY_HERE"  # ← CHANGE THIS

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1 style="color:#0f0; text-align:center; padding:50px; background:#000; font-family:Arial;">
      HVACFlow™ Live Chat<br>
      <a href="/demo" style="color:#0f0;">Open Demo</a>
    </h1>
    """

@app.get("/demo", response_class=HTMLResponse)
async def demo():
    return open("demo.html").read()
