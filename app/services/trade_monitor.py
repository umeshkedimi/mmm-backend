# app/services/trade_monitor.py

import asyncio
import datetime
from sqlalchemy.orm import Session
from app.db.db_setup import SessionLocal
from app.db.models.user import User
from app.db.models.broker_account import BrokerAccount
from app.services.dhan_service import get_live_pnl, exit_position
from app.utils.telegram import send_telegram_message

START_TIME = datetime.time(hour=9, minute=10)
END_TIME = datetime.time(hour=15, minute=35)

class TradeMonitorManager:
    def __init__(self):
        self.user_tasks = {}

    async def start_monitoring(self):
        print("🚀 Starting Trade Monitor Manager...")
        while True:
            now = datetime.datetime.now().time()
            if START_TIME <= now <= END_TIME:
                await self._start_all_users()
            else:
                await self._stop_all_users()
            await asyncio.sleep(60)

    async def _start_all_users(self):
        db = SessionLocal()
        try:
            users = db.query(User).filter(User.is_active == True).all()
            for user in users:
                if user.id not in self.user_tasks:
                    print(f"✅ Starting monitor for user: {user.username}")
                    self.user_tasks[user.id] = asyncio.create_task(self._monitor_user(user))
        finally:
            db.close()

    async def _stop_all_users(self):
        for user_id, task in self.user_tasks.items():
            print(f"🛑 Stopping monitor for user ID {user_id}")
            task.cancel()
        self.user_tasks.clear()

    async def _monitor_user(self, user: User):
        db = SessionLocal()
        try:
            broker_account: BrokerAccount = db.query(BrokerAccount).filter(
                BrokerAccount.user_id == user.id
            ).first()

            if not broker_account:
                print(f"❌ No broker account for user: {user.username}")
                return

            while True:
                try:
                    pnl, sl, target = await get_live_pnl(broker_account)
                    print(f"📈 {user.username} → PnL: ₹{pnl} | SL: ₹{sl} | Target: ₹{target}")

                    if pnl <= -sl:
                        await exit_position(broker_account)
                        await send_telegram_message(user.username, f"🛑 SL Hit! Exiting positions.")
                        break

                    elif pnl >= target:
                        await exit_position(broker_account)
                        await send_telegram_message(user.username, f"✅ Target Hit! Booking profits.")
                        break

                    await asyncio.sleep(15)
                except asyncio.CancelledError:
                    print(f"🔁 Monitor cancelled for {user.username}")
                    break
        finally:
            db.close()
