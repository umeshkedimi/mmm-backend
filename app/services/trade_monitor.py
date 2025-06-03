import asyncio
from datetime import datetime, time
from app.db.models.broker_account import BrokerAccount
from app.db.models.user import User
from app.db.db_setup import SessionLocal
from app.services.broker.dhan import get_pnl, exit_all_positions  # Placeholder functions
from app.utils.telegram import send_telegram_message  # Optional
from sqlalchemy.orm import Session

async def monitor_single_user(user_id: int, broker: BrokerAccount):
    session: Session = SessionLocal()

    try:
        print(f"🔍 Monitoring started for user_id: {user_id} | {broker.index} | {broker.direction}")

        while True:
            now = datetime.now().time()

            # Stop monitoring after 3:35 PM
            if now > time(15, 35):
                print(f"⏹️ Monitoring ended for user_id: {user_id}")
                break

            # Optional: Add market open condition
            if now < time(9, 10):
                await asyncio.sleep(5)
                continue

            # Fetch PnL
            pnl = get_pnl(broker)  # Implemented separately per broker
            print(f"📈 User {user_id} PnL: ₹{pnl:.2f}")

            # Check SL or Target
            if broker.stop_loss and pnl <= -broker.stop_loss:
                print(f"🛑 SL Hit for user {user_id} → Exiting")
                exit_all_positions(broker)
                send_telegram_message(broker.telegram_chat_id, "🚨 Stop Loss hit. Position exited.")
                break

            if broker.target and pnl >= broker.target:
                print(f"🎯 Target Hit for user {user_id} → Exiting")
                exit_all_positions(broker)
                send_telegram_message(broker.telegram_chat_id, "✅ Target achieved. Position exited.")
                break

            await asyncio.sleep(5)  # Wait before next check

    except Exception as e:
        print(f"❌ Error while monitoring user {user_id}: {e}")

    finally:
        session.close()
