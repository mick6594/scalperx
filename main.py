from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pytz

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "updated": datetime.now(pytz.timezone("Australia/Brisbane")).strftime('%Y-%m-%d %H:%M:%S')
    })

@app.get("/signals")
async def get_signals():
    # Dummy signal data for testing UI
    return [
        {
            "coin": "BTCUSDT",
            "direction": "Long",
            "confidence": 91,
            "entry": 67420.25,
            "tp": 67700.25,
            "sl": 67200.00
        },
        {
            "coin": "ETHUSDT",
            "direction": "Short",
            "confidence": 85,
            "entry": 3725.00,
            "tp": 3680.00,
            "sl": 3740.00
        },
        {
            "coin": "SOLUSDT",
            "direction": "Long",
            "confidence": 94,
            "entry": 146.25,
            "tp": 150.00,
            "sl": 144.50
        },
        {
            "coin": "DOGEUSDT",
            "direction": "Short",
            "confidence": 87,
            "entry": 0.122,
            "tp": 0.119,
            "sl": 0.124
        }
    ]