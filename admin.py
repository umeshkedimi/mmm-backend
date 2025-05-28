import streamlit as st
import requests
import pandas as pd

# Config
API_URL = "http://localhost:8000"  # Change if deployed remotely

st.set_page_config(page_title="MMM Admin Dashboard", layout="wide")
st.title("📊 MMM Admin Dashboard")

# --- Session State Defaults ---
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "headers" not in st.session_state:
    st.session_state.headers = {}
if "users_df" not in st.session_state:
    st.session_state.users_df = None

# --- Sidebar Login Form ---
with st.sidebar:
    st.header("🔐 Admin Login")
    if st.session_state.access_token:
        st.success("✅ Logged in as Admin")
        if st.button("🚪 Logout"):
            st.session_state.access_token = None
            st.session_state.headers = {}
            st.session_state.users_df = None
            st.rerun()
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                login_res = requests.post(f"{API_URL}/auth/login", json={
                    "username": username,
                    "password": password
                })

                if login_res.status_code == 200:
                    token = login_res.json()["access_token"]
                    st.session_state.access_token = token
                    st.session_state.headers = {"Authorization": f"Bearer {token}"}
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {login_res.text}")

# --- Helper Function ---
def get_data(endpoint):
    token = st.session_state.get("access_token")
    if not token:
        st.warning("Please login first.")
        return None
    try:
        response = requests.get(
            f"{API_URL}/admin/{endpoint}",
            headers=st.session_state.headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# --- 2. System Metrics ---
if st.session_state.access_token:
    st.subheader("📈 System Metrics")
    metrics = get_data("metrics")
    if metrics:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", metrics["total_users"])
        col2.metric("Active Users", metrics["active_users"])
        col3.metric("Total Trades", metrics["total_trades"])

    # --- 3. Users Table ---
    st.subheader("👥 All Users")

    if st.session_state.users_df is None:
        users = get_data("users")
        if users:
            st.session_state.users_df = pd.DataFrame(users)

    if st.session_state.users_df is not None:
        st.dataframe(st.session_state.users_df)

        # --- Kill Switch Control ---
        user_ids = [
            f"{row['id']} - {row['username']}"
            for row in st.session_state.users_df.to_dict("records")
        ]
        selected_user = st.selectbox("Select user to toggle Kill Switch", user_ids)
        selected_user_id = int(selected_user.split(" - ")[0])
        action = st.radio("Set Kill Switch to:", ["True", "False"], horizontal=True)

        if st.button("Update Kill Switch"):
            payload = {
                "user_id": selected_user_id,
                "status": True if action == "True" else False
            }
            res = requests.post(f"{API_URL}/admin/killswitch", headers=st.session_state.headers, json=payload)
            if res.status_code == 200:
                st.success("Kill switch updated.")
                users = get_data("users")
                if users:
                    st.session_state.users_df = pd.DataFrame(users)
            else:
                st.error(f"Failed: {res.status_code} - {res.text}")

    # --- 4. Trade Logs ---
    st.subheader("💼 Trade Logs")
    trades = get_data("trades")
    if trades:
        trades_df = pd.DataFrame(trades)
        st.dataframe(trades_df)
