from services.kite_service import get_kite
import logging

kite = get_kite()
logger = logging.getLogger(__name__)

def get_pnl():
    try:
        positions = kite.positions()["net"]
        if len(positions) == 0:
            return {"pnl": 0.0, "message": "No positions open."}

        symbol_list = []
        for pos in positions:
            symbol = f"{pos['exchange']}:{pos['tradingsymbol']}"
            if symbol not in symbol_list:
                symbol_list.append(symbol)

        ltp_data = kite.ltp(symbol_list)

        total_pnl = 0
        for pos in positions:
            if pos["quantity"] != 0:
                symbol = f"{pos['exchange']}:{pos['tradingsymbol']}"
                ltp = ltp_data[symbol]["last_price"]
                pnl = (
                    pos["sell_price"] * pos["sell_quantity"]
                    - pos["buy_price"] * pos["buy_quantity"]
                    + ltp * (pos["buy_quantity"] - pos["sell_quantity"])
                )
            else:
                pnl = pos["pnl"]

            total_pnl += pnl

        return {"pnl": round(total_pnl, 2)}
    except Exception as e:
        logger.error(f"Error fetching PnL: {e}")
        return {"error": str(e)}
