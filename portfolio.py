def simulate_portfolio(data,predictor):
    holdings = data.get("holdings",[])
    days_ahead = data.get("days_ahead",1)
    results=[]
    for h in holdings:
        sym = h["symbol"]
        amt = h["amount"]
        pred = predictor.predict(sym,days_ahead)
        results.append({
            "symbol": sym,
            "amount": amt,
            "predicted_value": round(pred*amt,4)
        })
    total = sum([r["predicted_value"] for r in results])
    return {"holdings":results,"total_predicted":round(total,4)}
