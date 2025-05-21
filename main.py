from fastapi import FastAPI
from routers import trade_routes
import uvicorn

app = FastAPI(
    title="BankNifty MCP Server",
    description="A modular MCP server to manage BankNifty trades using Zerodha kite API",
    version="1.0.0"
)

app.include_router(trade_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)