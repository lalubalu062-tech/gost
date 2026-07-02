from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ye landing page dikhayega
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ye Ghost Proxy hai jo chup-chap dusra blog layega
@app.get("/proxy-browser")
async def fetch_blog(request: Request, target_url: str):
    client_ip = request.client.host
    headers = {
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
        "X-Forwarded-For": client_ip, 
        "X-Real-IP": client_ip
    }
    try:
        response = requests.get(target_url, headers=headers)
        return HTMLResponse(content=response.text)
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
