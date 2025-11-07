import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pendle_utils import fetch_pendle_markets, fetch_market_by_id
from ai_models import PricePredictor
from portfolio import simulate_portfolio
from backtest import backtest
from ascii_charts import plot_prices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Pendle_MCP")

app = FastAPI(title="Pendle_MCP", version="1.0.0", description="AI + Pendle MCP")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

predictor = PricePredictor()
predictor.load_or_train()

DEFAULT_CHAIN = "arbitrum"

class PredictRequest(BaseModel):
    symbol: str
    days_ahead: int = 1
    lookback_days: int = 90

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/markets")
async def markets(chain: str = DEFAULT_CHAIN, first: int = 50, skip: int = 0):
    try:
        data = await fetch_pendle_markets(chain=chain, first=first, skip=skip)
        return {"source": "subgraph", "chain": chain, "count": len(data), "pairs": data}
    except Exception as e:
        logger.exception("Failed to fetch markets: %s", e)
        return {"error": str(e), "pairs": []}

@app.get("/market/{market_id}")
async def market_by_id(market_id: str, chain: str = DEFAULT_CHAIN):
    try:
        pair = await fetch_market_by_id(chain=chain, market_id=market_id)
        if not pair:
            raise HTTPException(status_code=404, detail="Market not found")
        return {"pair": pair}
    except Exception as e:
        logger.exception("Error fetching market: %s", e)
        raise HTTPException(status_code=500, detail="internal error")

@app.post("/predict")
async def predict(req: PredictRequest):
    pred_price = predictor.predict(req.symbol, req.days_ahead, req.lookback_days)
    current_price = max(pred_price * 0.98, 0.01)
    change_pct = (pred_price - current_price)/current_price*100
    if change_pct > 3: signal, risk, confidence = "BUY","Moderate risk","0.8"
    elif change_pct < -3: signal, risk, confidence = "SELL","High risk","0.8"
    else: signal, risk, confidence = "HOLD","Neutral","0.5"
    return {
        "symbol": req.symbol,
        "days_ahead": req.days_ahead,
        "predicted_price": round(pred_price,8),
        "signal": signal,
        "confidence": float(confidence),
        "risk_note": risk
    }

@app.post("/simulate_portfolio")
async def simulate(data: dict):
    try:
        result = simulate_portfolio(data, predictor)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backtest")
async def run_backtest(data: dict):
    symbol = data.get("symbol")
    lookback = data.get("lookback_days",90)
    forecast = data.get("forecast_days",7)
    result = backtest(symbol, predictor, lookback_days=lookback, forecast_days=forecast)
    history = [h["actual"] for h in result["history"]]
    predicted = [h["predicted"] for h in result["history"]]
    plot_prices(history, predicted, title=f"Backtest {symbol}")
    return result

@app.post("/predict_multi")
async def predict_multi(data: dict):
    symbol = data.get("symbol")
    days_list = data.get("days",[1])
    result=[]
    for d in days_list:
        pred = predictor.predict(symbol, days_ahead=d)
        result.append({"day_ahead":d,"predicted_price":round(pred,4)})
    return {"symbol":symbol,"predictions":result}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.getenv("PORT",8000)), reload=True)


