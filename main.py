from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import requests

app = FastAPI()

# Ye seedha HTML file dikhayega (Jinja2 ka error ab nahi aayega)
@app.get("/")
async def home():
    return FileResponse("templates/index.html")

# Ye Ghost Proxy hai jo chup-chap dusra blog layega
@app.get("/proxy-browser")
async def fetch_blog(request: Request, target_url: str):
    client_ip = request.client.host
    headers = {
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0"),
        "X-Forwarded-For": client_ip, 
        "X-Real-IP": client_ip
    }
    try:
        response = requests.get(target_url, headers=headers)
        return HTMLResponse(content=response.text)
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
