import httpx
import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import math

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🟢 Fetch data from Binance Futures
async def fetch_binance_prices():
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return []
        return response.json()

# 🟢 Simulate signals with confidence, TP, SL
async def generate_signals():
    data = await fetch_binance_prices()
    signals = []

    for item in data:
        symbol = item["symbol"]
        if not symbol.endswith("USDT"):
            continue

        price = float(item["price"])
        direction = "Long" if hash(symbol) % 2 == 0 else "Short"
        confidence = round(abs(math.sin(hash(symbol))) * 100 % 100, 1)

        tp = price * (1 + 0.04) if direction == "Long" else price * (1 - 0.04)
        sl = price * (1 - 0.02) if direction == "Long" else price * (1 + 0.02)

        signals.append({
            "symbol": symbol,
            "direction": direction,
            "confidence": confidence,
            "entry": round(price, 3),
            "tp": round(tp, 3),
            "sl": round(sl, 3),
            "time": datetime.now().strftime("%H:%M:%S")  # Use local time
        })

    # 🟢 Sort by confidence DESCENDING
    return sorted(signals, key=lambda x: x["confidence"], reverse=True)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        signals = await generate_signals()
        longs = [s for s in signals if s["direction"] == "Long"]
        shorts = [s for s in signals if s["direction"] == "Short"]
        return templates.TemplateResponse("index.html", {
            "request": request,
            "longs": longs,
            "shorts": shorts
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "longs": [], "shorts": []})