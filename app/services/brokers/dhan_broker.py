import requests
from app.db.models.broker_account import BrokerAccount
from app.utils.broker_utils import get_atm_strike  # Assume you have this utility function

# Optional: Add your own logger if needed
import logging
logger = logging.getLogger(__name__)


# Helper: Dhan API base and headers
def get_dhan_headers(broker: BrokerAccount):
    return {
        "accept": "application/json",
        "access-token": broker.access_token,
        "Content-Type": "application/json",
    }


# --- Get PnL ---
def get_pnl(broker: BrokerAccount) -> float:
    try:
        url = "https://api.dhan.co/positions"  # Assumed endpoint
        headers = get_dhan_headers(broker)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        positions = response.json()

        total_pnl = 0.0
        for pos in positions:
            if pos.get("netQty", 0) != 0:
                total_pnl += float(pos.get("realizedProfitLoss", 0)) + float(pos.get("unrealizedProfitLoss", 0))

        logger.info(f"[DHAN] Total PnL for user {broker.client_id}: ₹{total_pnl:.2f}")
        return total_pnl

    except Exception as e:
        logger.error(f"[DHAN] Error fetching PnL: {e}")
        return 0.0


# --- Exit All Positions ---
def exit_all_positions(broker: BrokerAccount):
    try:
        # 1. Cancel all open orders
        orders_url = "https://api.dhan.co/orders"
        headers = get_dhan_headers(broker)
        orders_resp = requests.get(orders_url, headers=headers)
        orders_resp.raise_for_status()
        orders = orders_resp.json()

        for order in orders:
            if order["status"] in ["OPEN", "TRIGGER PENDING"]:
                cancel_url = f"https://api.dhan.co/orders/{order['orderId']}"
                requests.delete(cancel_url, headers=headers)

        logger.info(f"✅ [DHAN] Open orders cancelled for user {broker.client_id}")

        # 2. Square off open positions
        positions_url = "https://api.dhan.co/positions"
        pos_resp = requests.get(positions_url, headers=headers)
        pos_resp.raise_for_status()
        positions = pos_resp.json()

        for pos in positions:
            if pos.get("netQty", 0) != 0:
                square_off_url = "https://api.dhan.co/squareoff"
                payload = {
                    "securityId": pos["securityId"],
                    "exchangeSegment": pos["exchangeSegment"],
                    "productType": pos["productType"],
                    "transactionType": "SELL" if pos["netQty"] > 0 else "BUY",
                    "quantity": abs(pos["netQty"]),
                }
                requests.post(square_off_url, json=payload, headers=headers)

        logger.info(f"✅ [DHAN] Positions squared off for user {broker.client_id}")
        return {"status": "success"}

    except Exception as e:
        logger.error(f"❌ [DHAN] Kill switch failed: {e}")
        return {"error": str(e)}


# --- Place ATM Option Order ---
def place_order(broker: BrokerAccount, option_type: str) -> dict:
    """
    Places an ATM CE/PE market order.
    :param broker: BrokerAccount object
    :param option_type: "CE" or "PE"
    """
    try:
        # Step 1: Get ATM Option Symbol from broker.index ("nifty" or "banknifty")
        # For now, hardcoded dummy symbols — in production, fetch dynamically or from DB
        if broker.index.lower() == "banknifty":
            symbol = get_atm_strike(broker)  # Dummy CE/PE symbol
        elif broker.index.lower() == "nifty":
            symbol = get_atm_strike(broker)  # Dummy CE/PE symbol
        else:
            raise ValueError("Invalid index")

        transaction_type = "BUY" if broker.direction == "buy" else "SELL"
        if option_type.upper() == "PE":
            symbol = symbol.replace("CE", "PE")
        elif option_type.upper() == "CE":
            symbol = symbol.replace("PE", "CE")

        url = "https://api.dhan.co/orders"
        headers = get_dhan_headers(broker)
        payload = {
            "securityId": symbol,
            "exchangeSegment": "NSE_OPTIDX",
            "transactionType": transaction_type,
            "quantity": broker.lot_size,
            "orderType": "MARKET",
            "productType": "INTRADAY",
            "price": 0,
            "validity": "DAY",
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        logger.info(f"✅ [DHAN] Order placed: {transaction_type} {symbol} x {broker.lot_size}")
        return response.json()

    except Exception as e:
        logger.error(f"❌ [DHAN] Order failed: {e}")
        return {"error": str(e)}

# --- Disable Kill Switch ---
def disable_killswitch(broker: BrokerAccount) -> dict:
    """
    Calls Dhan API to disable the kill switch if supported.
    """
    try:
        url = "https://api.dhan.co/disable-killswitch"  # Replace with actual endpoint if different
        headers = get_dhan_headers(broker)

        response = requests.post(url, headers=headers)
        response.raise_for_status()

        logger.info(f"✅ [DHAN] Kill switch disabled for user {broker.client_id}")
        return {"status": "disabled"}

    except Exception as e:
        logger.error(f"❌ [DHAN] Failed to disable kill switch: {e}")
        return {"error": str(e)}
