from fastapi import FastAPI
import uvicorn
import threading
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv(override=True)

# ✅ Validate critical env config
def validate_config():
    required_keys = ["DRY_RUN", "API_KEY_HEADER"]
    for key in required_keys:
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"❌ {key} is missing in .env file!")
    print(f"✅ DRY_RUN = {os.getenv('DRY_RUN')}")
    print("✅ Environment variables loaded successfully.")

validate_config()

# ✅ Import after env is loaded
from app.routers import trade_routes, auth_routes
from app.services.trade_watcher import monitor_trades

app = FastAPI(
    title="BankNifty MCP Server",
    description="A modular MCP server to manage BankNifty trades using Zerodha kite API",
    version="1.0.0"
)

app.include_router(trade_routes.router)
app.include_router(auth_routes.router)

# ✅ Start watcher thread
watcher_thread = threading.Thread(target=monitor_trades, daemon=True)
watcher_thread.start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
