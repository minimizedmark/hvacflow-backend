from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Enable CORS (fixes fetch errors)
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
    <head><title>HVACFlow.app</title></head>
    <body style="background:#000;color:#0f0;font-family:Arial;margin:0;padding:20px;">
      <h1>HVACFlow™</h1>
      <div id="chat" style="height:70vh;overflow:auto;border:1px solid #0f0;padding:10px;background:#111;border-radius:8px;"></div>
      <input id="input" placeholder="AC not cooling?" style="width:100%;padding:12px;background:#111;color:#0f0;border:1px solid #0f0;margin-top:10px;border-radius:8px;font-size:16px;" />
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
            return data.reply || "No response from server.";
          } catch (e) {
            return "Network error: " + e.message;
          }
        }

        input.onkeypress = async (e) => {
          if (e.key === 'Enter' && input.value.trim()) {
            const msg = input.value.trim();
            chat.innerHTML += `<p style="margin:8px 0;"><b>You:</b> ${msg}</p>`;
            input.value = '';
            chat.innerHTML += `<p style="margin:8px 0; color:#888;"><i>HVACFlow™ is thinking...</i></p
