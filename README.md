#PENDLE MCP

**AI-powered Market Command Protocol (MCP) for Pendle on Arbitrum**

This MCP package includes:

- Real Pendle market data from Arbitrum subgraph
- AI price predictions (multi-day)
- Risk scoring & confidence signals
- Portfolio simulation
- Backtesting with ASCII charts
- MCP Inspector support

---

## ⚡ Setup

1. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the server

bash
Copy code
uvicorn server:app --reload --port 8000
Run MCP Inspector

bash
Copy code
npx @modelcontextprotocol/inspector
🛠️ Usage
Health check
bash
Copy code
GET /health
List Pendle markets
sql
Copy code
GET /markets?first=50
Get market by ID
bash
Copy code
GET /market/{market_id}
Price prediction
css
Copy code
POST /predict
Body: {"symbol":"ETH","days_ahead":1}
Multi-day prediction
css
Copy code
POST /predict_multi
Body: {"symbol":"ETH","days":[1,3,5,7]}
Simulate portfolio
css
Copy code
POST /simulate_portfolio
Body: {"holdings":[{"symbol":"ETH","amount":10}],"days_ahead":3}
Backtest predictions
css
Copy code
POST /backtest
Body: {"symbol":"ETH","lookback_days":90,"forecast_days":7}
✅ Testing
Run all tests using pytest:

bash
Copy code
pytest tests/
Example test files included:

tests/test_endpoints.py → Tests API endpoints

tests/test_portfolio.py → Tests portfolio simulation

📈 Features
Terminal ASCII charts for price trends and predictions

AI-powered predictions for 1,3,5,7 days ahead

Dynamic confidence & risk scoring

Portfolio simulation with predicted returns

Backtesting module to evaluate prediction accuracy

Fully MCP Inspector-compatible

Expandable architecture for future DeFi integrations

⚙️ Recommended Usage
Always run in a virtual environment to avoid dependency conflicts

For backtesting, start with lookback_days=90 and forecast_days=7

Use predict_multi for multi-day forecasts in portfolios

Check ASCII charts for visual trends in terminal

📌 Notes
This version uses synthetic historical prices for AI backtesting

Future upgrades can integrate real OHLC Pendle historical data for more accurate predictions

Designed to run on Arbitrum mainnet, read-only mode by default