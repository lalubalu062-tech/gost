from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import requests

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("templates/index.html")

# Ghost Proxy - Strict Referrer Controller
@app.get("/proxy-browser")
async def fetch_blog(request: Request, target_url: str, referer_url: str = None):
    client_ip = request.client.host
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Forwarded-For": client_ip, 
        "X-Real-IP": client_ip
    }
    
    # Agar frontend se koi referer bheja hai toh wahi lagao, 
    # Nahi toh Render ka khud ka URL default referer banega
    if referer_url:
        headers["Referer"] = referer_url
    else:
        headers["Referer"] = str(request.base_url)
        
    try:
        response = requests.get(target_url, headers=headers)
        return HTMLResponse(content=response.text)
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
        
