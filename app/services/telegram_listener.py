import asyncio
from datetime import datetime, time

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.error import TimedOut

from app.db.db_setup import SessionLocal
from app.db.models.broker_account import BrokerAccount
from app.db.models.user import User
from app.services.brokers.dhan_broker import (
    place_order,
    get_pnl,
    exit_all_positions,
    disable_killswitch,
)
from app.utils.broker_utils import get_atm_strike


# === Handle Commands ===
async def handle_command(command: str, broker: BrokerAccount, user: User) -> str:
    if not broker.is_active:
        return "❌ You are not an active user."

    now = datetime.now().time()
    allowed_time = time(9, 15) <= now <= time(15, 15)

    if command == "buy":
        if not allowed_time:
            return "⏱️ Command allowed between 9:15 AM – 3:15 PM."
        option_type = "CE" if broker.direction == "buy" else "PE"
        symbol = get_atm_strike(broker.index, option_type)
        place_order(broker, symbol, "BUY")
        return f"🟢 BUY order placed: {symbol} (Direction: {broker.direction.upper()})"

    elif command == "sell":
        if not allowed_time:
            return "⏱️ Command allowed between 9:15 AM – 3:15 PM."
        option_type = "PE" if broker.direction == "buy" else "CE"
        symbol = get_atm_strike(broker.index, option_type)
        place_order(broker, symbol, "SELL")
        return f"🔴 SELL order placed: {symbol} (Direction: {broker.direction.upper()})"

    elif command == "pnl":
        pnl = get_pnl(broker)
        return f"📊 Current PnL: ₹{pnl:.2f}"

    elif command == "kill":
        if not allowed_time:
            return "⏱️ Command allowed between 9:15 AM – 3:15 PM."
        exit_all_positions(broker)
        disable_killswitch(broker)
        return "💀 Kill switch activated. Positions exited and kill disabled."

    elif command == "hello":
        return f"👋 Hello, {user.username}!"

    elif command == "tradeinfo":
        return (
            f"📋 Trade Info:\n"
            f"Index: {broker.index}\n"
            f"Direction: {broker.direction}\n"
            f"Target: ₹{broker.target}\n"
            f"Stop Loss: ₹{broker.stop_loss}\n"
            f"Lot Size: {broker.lot_size}"
        )

    elif command == "help":
        return (
            "🛠️ Available Commands:\n"
            "/buy – Place ATM CE/PE based on direction\n"
            "/sell – Place opposite side ATM order\n"
            "/pnl – Show current PnL\n"
            "/kill – Exit all positions + disable kill\n"
            "/hello – Greet\n"
            "/tradeinfo – Show trade config\n"
            "/help – Show commands"
        )

    return "❌ Unknown command. Use /help."


# === Generate Command Handlers ===
def generate_command_handler(broker: BrokerAccount, user: User):
    async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        command = update.message.text.strip().lstrip("/").lower()
        response = await handle_command(command, broker, user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    return command_handler


# === Run Bots for All Active Users ===
async def run_telegram_bot():
    await asyncio.sleep(3)  # Allow DB to fully initialize

    session = SessionLocal()
    brokers = session.query(BrokerAccount).filter(BrokerAccount.is_active == True).all()

    print(f"🤖 Launching {len(brokers)} Telegram bots...")

    for broker in brokers:
        user = session.query(User).filter(User.id == broker.user_id).first()
        if not broker.telegram_bot_token or not broker.telegram_chat_id:
            print(f"⚠️ Skipping user {user.username} (missing bot token or chat_id)")
            continue

        try:
            application = ApplicationBuilder().token(broker.telegram_bot_token).build()

            # Add handlers for all commands
            for cmd in ["buy", "sell", "pnl", "kill", "hello", "tradeinfo", "help"]:
                handler = CommandHandler(cmd, generate_command_handler(broker, user))
                application.add_handler(handler)

            # Initialize and start the bot
            await application.initialize()
            await application.start()
            asyncio.create_task(application.updater.start_polling())

            print(f"✅ Bot started for {user.username} | Chat ID: {broker.telegram_chat_id}")

        except TimedOut:
            print(f"❌ Timed out while starting bot for {user.username}")
        except Exception as e:
            print(f"❌ Error for {user.username}: {str(e)}")

        await asyncio.sleep(1)  # Slight delay before next bot

    session.close()
