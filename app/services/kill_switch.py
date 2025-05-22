from app.services.kite_service import get_kite
import logging

kite = get_kite()
logger = logging.getLogger(__name__)

def activate_kill_switch():
    try:
        # 1. Cancel all open/pending orders
        orders = kite.orders()
        for order in orders:
            if order["status"] in ["OPEN", "TRIGGER PENDING"]:
                kite.cancel_order(variety=order["variety"], order_id=order["order_id"])
        logger.info("✅ All open orders cancelled.")

        # 2. Square off all open positions
        positions = kite.positions()["net"]
        for pos in positions:
            if pos["quantity"] != 0:
                kite.place_order(
                    variety=kite.VARIETY_REGULAR,
                    exchange=pos["exchange"],
                    tradingsymbol=pos["tradingsymbol"],
                    transaction_type=kite.TRANSACTION_TYPE_SELL if pos["quantity"] > 0 else kite.TRANSACTION_TYPE_BUY,
                    quantity=abs(pos["quantity"]),
                    product=pos["product"],
                    order_type=kite.ORDER_TYPE_MARKET,
                )
        logger.info("✅ All positions squared off.")
        return {"status": "success", "message": "Kill switch activated. Positions squared off and orders cancelled."}

    except Exception as e:
        logger.error(f"❌ Kill switch failed: {e}")
        return {"error": str(e)}
