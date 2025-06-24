from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pytz
import httpx

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
    BINANCE_API = "https://fapi.binance.com/fapi/v1/ticker/price"

    async with httpx.AsyncClient() as client:
        res = await client.get(BINANCE_API)
        prices = res.json()

    # Filter only USDT pairs (no BUSD, etc.)
    usdt_pairs = [p for p in prices if p["symbol"].endswith("USDT") and not p["symbol"].endswith("BUSD")]

    signals = []
    for i, p in enumerate(usdt_pairs[:100]):  # Limit for performance
        price = float(p["price"])
        direction = "Long" if i % 2 == 0 else "Short"
        confidence = round(88 + (i % 10) + (i * 0.05), 2)
        tp = price * (1.03 if direction == "Long" else 0.97)
        sl = price * (0.97 if direction == "Long" else 1.03)
        signals.append({
            "coin": p["symbol"],
            "direction": direction,
            "confidence": confidence,
            "entry": round(price, 4),
            "tp": round(tp, 4),
            "sl": round(sl, 4)
        })

    return sorted(signals, key=lambda x: x["confidence"], reverse=True)
