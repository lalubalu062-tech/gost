from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import requests

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("templates/index.html")

# Ghost Proxy - Strict Referrer & Real User-Agent Controller
@app.get("/proxy-browser")
async def fetch_blog(request: Request, target_url: str, referer_url: str = None):
    client_ip = request.client.host
    
    # 🕵️‍♂️ Asli user ka User-Agent nikalna (Agar kisi wajah se na mile toh default use karega)
    real_user_agent = request.headers.get("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    headers = {
        "User-Agent": real_user_agent,  # Ab har user ka apna asli phone/PC ka detail jayega!
        "X-Forwarded-For": client_ip, 
        "X-Real-IP": client_ip
    }
    
    # Referer set karna
    if referer_url:
        headers["Referer"] = referer_url
    else:
        headers["Referer"] = str(request.base_url)
        
    try:
        response = requests.get(target_url, headers=headers)
        return HTMLResponse(content=response.text)
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
