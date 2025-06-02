# app/services/dhan_service.py

import httpx
import os

DHAN_BASE_URL = "https://api.dhan.co"

HEADERS_TEMPLATE = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# You can update these if different endpoints or headers are needed
def get_dhan_headers(access_token: str):
    headers = HEADERS_TEMPLATE.copy()
    headers["access-token"] = access_token
    return headers


async def get_live_pnl(broker_account):
    """
    Fetch live PnL from Dhan API.
    Assumes single active position in BankNifty
    """
    url = f"{DHAN_BASE_URL}/positions"
    headers = get_dhan_headers(broker_account.access_token)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch positions for {broker_account.client_id}")
        return 0, broker_account.stop_loss, broker_account.target

    positions = response.json().get("data", [])
    net_pnl = 0
    for pos in positions:
        if pos["exchangeSegment"] == "NSE" and pos["productType"] == "INTRADAY":
            net_pnl += float(pos.get("realizedProfitLoss", 0)) + float(pos.get("unrealizedProfitLoss", 0))

    return net_pnl, broker_account.stop_loss, broker_account.target


async def exit_position(broker_account):
    """
    Exit all open positions for user via Dhan API
    """
    url = f"{DHAN_BASE_URL}/positions/intraday"
    headers = get_dhan_headers(broker_account.access_token)

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"✅ Positions closed for {broker_account.client_id}")
    else:
        print(f"❌ Failed to close positions: {response.text}")
