# main.py

import os
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv

# ✅ Load environment variables first
load_dotenv(override=True)

# ✅ Validate critical config
def validate_config():
    required_keys = ["DRY_RUN", "API_KEY_HEADER"]
    for key in required_keys:
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"❌ {key} is missing in .env file!")
    print(f"✅ DRY_RUN = {os.getenv('DRY_RUN')}")
    print("✅ Environment variables loaded successfully.")

validate_config()

# ✅ Delayed imports (after env is loaded)
from app.routers import auth_routes, broker_account
from app.services.trade_monitor import monitor_all_users
from app.services.telegram_listener import run_telegram_bot

# ✅ Initialize FastAPI app
app = FastAPI(
    title="BankNifty MCP Server",
    description="A modular MCP server to manage BankNifty trades using Zerodha/Dhan API",
    version="1.0.0",
    openapi_tags=[
        {"name": "Auth", "description": "User registration and login"},
        {"name": "Broker Accounts", "description": "Manage linked broker accounts"},
    ]
)

# ✅ Register routers
app.include_router(auth_routes.router)
app.include_router(broker_account.router)

# ✅ Start background trade monitor on app startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_all_users())
    asyncio.create_task(run_telegram_bot())

# ✅ Run via `uvicorn main:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
