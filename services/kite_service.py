import os
import pyotp
import requests
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

kite = KiteConnect(api_key=os.getenv("API_KEY"))

def get_access_token():
    session = requests.Session()

    user_id = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    totp_token = os.getenv("TOTP_TOKEN")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    # Login Step 1
    login_res = session.post("https://kite.zerodha.com/api/login", {
        "user_id": user_id,
        "password": password
    }).json()

    request_id = login_res["data"]["request_id"]

    # Login Step 2
    session.post("https://kite.zerodha.com/api/twofa", {
        "user_id": user_id,
        "request_id": request_id,
        "twofa_value": pyotp.TOTP(totp_token).now()
    })

    # Generate request token
    try:
        api_session = session.get(f"https://kite.trade/connect/login?api_key={api_key}")
        parsed = urlparse(api_session.url)
    except Exception as e:
        parsed = urlparse(e.request.url)

    request_token = parse_qs(parsed.query)["request_token"][0]

    # Generate access token
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    return access_token

def get_kite():
    access_token = get_access_token()
    kite.set_access_token(access_token)
    return kite