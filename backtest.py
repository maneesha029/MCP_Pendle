import numpy as np
from ai_models import PricePredictor

def backtest(symbol: str, predictor: PricePredictor, lookback_days=90, forecast_days=7):
    np.random.seed(abs(hash(symbol)) % (2**32))
    actual_prices = np.cumsum(np.random.randn(lookback_days+forecast_days) + 1.0)
    results = []
    correct_direction = 0
    for i in range(lookback_days):
        pred = predictor.predict(symbol, days_ahead=forecast_days, lookback_days=i+1)
        actual = actual_prices[i+forecast_days]
        signal = "BUY" if pred>actual_prices[i] else "SELL"
        correct_direction += (signal=="BUY" and actual>actual_prices[i]) or (signal=="SELL" and actual<actual_prices[i])
        results.append({"day": i+1,"predicted": round(pred,4),"actual": round(actual,4),"signal": signal})
    accuracy = correct_direction/lookback_days*100.0
    return {"symbol": symbol, "accuracy_percent": round(accuracy,2), "history": results}

