from app.db.models import User
from app.services.brokers import zerodha_broker, dhan_broker


def place_order(direction: str, user: User = None):
    if user:
        if user.broker == "zerodha":
            return zerodha_broker.place_order(direction, user)
        elif user.broker == "dhan":
            return dhan_broker.place_order(direction, user)
        else:
            raise Exception("Unsupported broker")
    else:
        # fallback for DRY_RUN or internal dev mode
        return zerodha_broker.place_order(direction)

