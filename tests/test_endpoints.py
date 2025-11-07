# tests/test_endpoints.py
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status":"ok"}

def test_markets():
    r = client.get("/markets?first=5")
    assert r.status_code == 200
    data = r.json()
    assert "pairs" in data
    assert isinstance(data["pairs"], list)

def test_predict():
    r = client.post("/predict", json={"symbol":"ETH","days_ahead":1})
    assert r.status_code == 200
    resp = r.json()
    assert "predicted_price" in resp
    assert "signal" in resp
