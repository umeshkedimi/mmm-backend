# app/utils/broker_utils.py

import requests
from app.db.models.broker_account import BrokerAccount

def get_atm_strike(broker: BrokerAccount) -> str:
    """
    Fetches ATM strike symbol for the given broker and index.
    E.g., BANKNIFTY2460635500 or NIFTY2460618000
    """
    headers = {
        "accept": "application/json",
        "access-token": broker.access_token,
    }

    if broker.index.lower() == "banknifty":
        security_id = "BANKNIFTY"
        round_to = 100
    elif broker.index.lower() == "nifty":
        security_id = "NIFTY"
        round_to = 50
    else:
        raise ValueError("Invalid index")

    # Get LTP
    try:
        url = f"https://api.dhan.co/market/quotes/latest/{security_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        ltp = float(data.get("lastTradedPrice", 0)) / 100  # price is in paise

        atm_strike = round(ltp / round_to) * round_to

        # Build option symbol (hardcoded expiry for now — replace with dynamic)
        expiry = "24606"  # June 6, 2024 (example)
        option_symbol = f"{security_id}{expiry}{int(atm_strike)}"

        return option_symbol

    except Exception as e:
        raise RuntimeError(f"Failed to fetch ATM strike for {security_id}: {e}")
