import os
import time
from services.kite_service import get_kite
from services.pnl_tracker import get_pnl
from services.kill_switch import activate_kill_switch

kite = get_kite()

TARGET = int(os.getenv("TARGET_PROFIT", 500))
SL = int(os.getenv("STOP_LOSS", -450))
TRAIL_STEP = int(os.getenv("TRAIL_STEP", 500))
TRAIL_GAP = int(os.getenv("TRAIL_GAP", 50))

trail_sl = SL
next_trail_target = TARGET + TRAIL_STEP

def monitor_trades():
    global trail_sl, next_trail_target
    print("🔍 Trade watcher started...")

    while True:
        pnl_data = get_pnl()
        if "pnl" not in pnl_data:
            time.sleep(5)
            continue

        pnl = pnl_data["pnl"]
        print(f"📈 Current PnL: ₹{pnl:.2f}")

        if pnl >= next_trail_target:
            trail_sl = pnl - TRAIL_GAP
            next_trail_target += TRAIL_STEP
            print(f"🔁 Trailing SL moved to ₹{trail_sl:.2f}")

        if pnl <= trail_sl:
            print(f"❌ SL Hit. Triggering Kill Switch...")
            activate_kill_switch()
            break

        time.sleep(5)
