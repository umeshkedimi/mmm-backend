import os
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

from app.db.models import User
import datetime
import logging
from sqlalchemy.orm import Session
from app.db.db_setup import get_db
from app.services.kite_service import get_kite
from app.db.crud.trade_log import create_trade_log
from app.db.schemas import TradeLogCreate

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
    
def place_order(trade_type: str, user: User = None):
    """
    Places a SELL order on ATM CE/PE depending on trade_type (buy/sell).
    - buy  => Sell PE (bullish view)
    - sell => Sell CE (bearish view)
    """
    expiry = get_banknifty_expiry()
    atm = get_atm_strike()
    
    if not expiry or not atm:
        return {"error": "Could not fetch expiry or strike"}

    option_type = "CE" if trade_type == "buy" else "PE"
    symbol = f"BANKNIFTY{expiry}{atm}{option_type}"

    print(f"📥 Broker: {user.broker}, Username: {user.username}")

    if DRY_RUN:
        logger.info(f"[DRY_RUN] Skipped placing order: {symbol}")
        return {"status": "dry_run", "symbol": symbol, "message": "trade skipped (dry run mode)"}

    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange="NFO",
            tradingsymbol=symbol,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=30,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )
        logger.info(f"✅ Order placed: {symbol}")

        db: Session = get_db()
        create_trade_log(db, TradeLogCreate(
            symbol=symbol,
            direction=trade_type,
            quantity=30,
            price=kite.ltp(f"NFO:{symbol}")[f"NFO: + {symbol}"]["last_price"],
            pnl=None,
            exit_reason=None
        ))

        return {"status": "success", "symbol": symbol, "order_id": order_id}
    except Exception as e:
        logger.error(f"❌ Failed to place order: {e}")
        return {"error": str(e)}