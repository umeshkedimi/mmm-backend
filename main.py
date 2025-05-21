from fastapi import FastAPI
from routers import trade_routes
import uvicorn
from services.trade_watcher import monitor_trades
import threading


app = FastAPI(
    title="BankNifty MCP Server",
    description="A modular MCP server to manage BankNifty trades using Zerodha kite API",
    version="1.0.0"
)

app.include_router(trade_routes.router)

# Start watcher thread
watcher_thread = threading.Thread(target=monitor_trades, daemon=True)
watcher_thread.start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)