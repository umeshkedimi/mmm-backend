import asyncio
from datetime import datetime, time
from sqlalchemy.orm import Session
from app.db.models.broker_account import BrokerAccount
from app.db.db_setup import SessionLocal
from app.services.broker.dhan import get_pnl, exit_all_positions  # Replace with real implementations
from app.utils.telegram import send_telegram_message


async def monitor_single_user(user_id: int, broker: BrokerAccount):
    """
    Monitor a single user's trade based on SL/Target from 9:10 AM to 3:35 PM.
    """
    session: Session = SessionLocal()

    try:
        print(f"🔍 Monitoring started for user_id: {user_id} | {broker.index} | {broker.direction}")

        while True:
            now = datetime.now().time()

            # Stop after market close
            if now > time(15, 35):
                print(f"⏹️ Monitoring ended for user_id: {user_id}")
                break

            # Wait for market open
            if now < time(9, 10):
                await asyncio.sleep(5)
                continue

            # Fetch PnL
            pnl = get_pnl(broker)  # Implement this in broker service
            print(f"📈 User {user_id} PnL: ₹{pnl:.2f}")

            # Check for SL
            if broker.stop_loss and pnl <= -broker.stop_loss:
                print(f"🛑 SL Hit for user {user_id} → Exiting")
                exit_all_positions(broker)
                send_telegram_message(broker.telegram_chat_id, "🚨 Stop Loss hit. Position exited.")
                break

            # Check for Target
            if broker.target and pnl >= broker.target:
                print(f"🎯 Target Hit for user {user_id} → Exiting")
                exit_all_positions(broker)
                send_telegram_message(broker.telegram_chat_id, "✅ Target achieved. Position exited.")
                break

            await asyncio.sleep(5)

    except Exception as e:
        print(f"❌ Error while monitoring user {user_id}: {e}")

    finally:
        session.close()


async def monitor_all_users():
    """
    Launch monitoring for all active broker accounts in parallel.
    """
    session: Session = SessionLocal()

    try:
        print("🚀 Launching background trade monitoring for all active users...")

        # Fetch all active broker accounts
        brokers = session.query(BrokerAccount).filter(BrokerAccount.is_active == True).all()

        tasks = []
        for broker in brokers:
            tasks.append(monitor_single_user(broker.user_id, broker))

        await asyncio.gather(*tasks)

    finally:
        session.close()
