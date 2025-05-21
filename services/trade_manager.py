from services.kite_service import get_kite
import datetime
import logging

kite = get_kite()
logger = logging.getLogger(__name__)

def get_banknifty_expiry():
    """Return nearest monthly expiry date in YYMMM format."""
    today = datetime.date.today()
    instruments = kite.instruments("NFO")

    expiry_dates = sorted(set(
        inst["expiry"] for inst in instruments
        if "BANKNIFTY" in inst["tradingsymbol"] and inst["segment"] == "NFO-OPT"
    ))

    for expiry in expiry_dates:
        if expiry >= today:
            return expiry.strftime("%y%b").upper()

    return None

def get_atm_strike():
    """Return rounded ATM strike of BankNifty."""
    try:
        ltp = kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"]
        return round(ltp / 100) * 100
    except Exception as e:
        logger.error(f"Error getting ATM: {e}")
        return None

def place_order(trade_type: str):
    """
    Places a SELL order on ATM CE/PE depending on trade_type (buy/sell).
    - buy  => Sell PE (bullish view)
    - sell => Sell CE (bearish view)
    """
    expiry = get_banknifty_expiry()
    atm = get_atm_strike()
    
    if not expiry or not atm:
        return {"error": "Could not fetch expiry or strike"}

    option_type = "PE" if trade_type == "buy" else "CE"
    symbol = f"BANKNIFTY{expiry}{atm}{option_type}"

    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange="NFO",
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=60,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )
        logger.info(f"✅ Order placed: {symbol}")
        return {"status": "success", "symbol": symbol, "order_id": order_id}
    except Exception as e:
        logger.error(f"❌ Failed to place order: {e}")
        return {"error": str(e)}
