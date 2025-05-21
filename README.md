# BankNifty MCP Server (Zerodha Kite + FastAPI)

This is a modular, production-style algo trading server built using FastAPI and Zerodha's Kite Connect API.

## Features

- Structured MCP architecture (modular backend)
- Live order placement for BankNifty (directional)
- `/buy`, `/sell`, and `/pnl` endpoints
- Integrated Kite Connect login with TOTP
- Kill switch logic (API-level)
- Public-ready project with secure `.env`

## Endpoints

| Method | Endpoint       | Description                    |
|--------|----------------|--------------------------------|
| GET    | `/trade/ping`  | Check server status            |
| POST   | `/trade/buy`   | Place BankNifty ATM PE order   |
| POST   | `/trade/sell`  | Place BankNifty ATM CE order   |
| GET    | `/trade/pnl`   | Show live PnL                  |
| POST   | `/trade/kill`  | Kill switch: Exit & Cancel all |

## Getting Started

```bash
git clone https://github.com/your-username/banknifty-mcp-server.git
cd banknifty-mcp-server
cp sample.env .env
# Fill in your Kite credentials in .env
pip install -r requirements.txt
python main.py


## Disclaimer

⚠️ This project is for educational and demonstration purposes only.  
Using real brokerage APIs with live capital involves risk.  
This project does **not** constitute financial advice or a guaranteed strategy.  
Use this system at your own discretion and **only in paper/live trading if you know what you are doing.**


## License

[MIT License](LICENSE)
