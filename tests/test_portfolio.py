# tests/test_portfolio.py
import pytest
from portfolio import simulate_portfolio
from ai_models import PricePredictor

def test_simulate_portfolio():
    predictor = PricePredictor()
    predictor.load_or_train()
    data = {
        "holdings":[{"symbol":"ETH","amount":10},{"symbol":"USDC","amount":50}],
        "days_ahead":1
    }
    result = simulate_portfolio(data, predictor)
    assert "holdings" in result
    assert "total_predicted" in result
    assert len(result["holdings"]) == 2
