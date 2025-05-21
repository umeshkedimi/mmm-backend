import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID"))
API_URL = os.getenv("MCP_API_URL")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_last_update_id():
    try:
        res = requests.get(f"{TELEGRAM_API_URL}/getUpdates").json()
        if "result" in res and res["result"]:
            return res["result"][-1]["update_id"]
    except Exception as e:
        print(f"Error fetching last update: {e}")
    return None

def send_msg(text):
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": text}
        response = requests.get(url, params=params)
        # Clean output
        if response.status_code == 200:
            print(f"✅ Message sent: {text}")
        else:
            print(f"❌ Failed to send message: {response.status_code} → {response.text}")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

def handle_command(text):
    text = text.strip().lower()

    if text == "buy":
        endpoint = "/trade/buy"
        method = "POST"
    elif text == "sell":
        endpoint = "/trade/sell"
        method = "POST"
    elif text == "pnl":
        endpoint = "/trade/pnl"
        method = "GET"
    elif text == "kill":
        endpoint = "/trade/kill"
        method = "POST"
    else:
        send_msg("⚠️ Invalid command! Use 'buy', 'sell', 'pnl', or 'kill'")
        return

    try:
        url = f"{API_URL}{endpoint}"
        headers = {"X-API-KEY": os.getenv("API_KEY_HEADER")}
        res = requests.request(method, url, headers=headers)
        
        if res.status_code == 200:
            send_msg(f"✅ {text.upper()} successful: {res.json()}")
        else:
            send_msg(f"❌ {text.upper()} failed: {res.status_code} - {res.text}")
    except Exception as e:
        send_msg(f"❌ Error: {e}")

def main():
    last_update_id = get_last_update_id()

    while True:
        try:
            params = {}
            if last_update_id:
                params["offset"] = last_update_id + 1

            response = requests.get(f"{TELEGRAM_API_URL}/getUpdates", params=params).json()

            if "result" in response:
                for msg in response["result"]:
                    last_update_id = msg["update_id"]
                    text = msg.get("message", {}).get("text", "")
                    print(f"[Telegram] {text}")
                    handle_command(text)

        except Exception as e:
            print(f"Telegram loop error: {e}")

        time.sleep(1)

if __name__ == "__main__":
    print("🔁 Telegram listener started...")
    send_msg("🤖 MCP Telegram Bot is active!")
    main()
