# HVACFlow™.app  
**AI-Powered 24/7 Chatbot for HVAC Contractors**  
`https://hvacflow.app` | `https://chat.hvacflow.app`

> **"Never miss a lead. Diagnose, book, and close — automatically."**  
> Powered by **Grok (xAI)** — No OpenAI. No censorship. $49/mo.

---

## Features
- 24/7 lead capture & emergency triage  
- Instant diagnostics (e.g., "AC leaking?")  
- Auto-booking with ZIP code  
- Embeddable widget (copy-paste on any site)  
- Fully customizable (logo, colors, prompts)  
- Voice-ready (Twilio + Grok Voice Mode)  

---

## Live Demo
**Try it now:** [https://chat.hvacflow.app](https://chat.hvacflow.app)  
Type: *"Furnace making banging noise — help!"*

---

## Quick Start (5 Minutes)

### 1. **Deploy Backend (Render.com)**
1. Fork this repo  
2. Go to [render.com](https://render.com) → New Web Service  
3. Connect your GitHub repo  
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variable**:# hvacflow-backend
