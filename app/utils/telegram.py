# app/utils/telegram.py

import httpx

async def send_telegram_message(chat_id: str, message: str, bot_token: str):
    """
    Sends a message to a Telegram user via a specific Telegram bot token.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code != 200:
        print(f"❌ Failed to send Telegram message: {response.text}")
