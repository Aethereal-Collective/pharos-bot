import requests
import time
from datetime import timedelta
from config import (
    sender_address,
)

from config_header import headers


def check_signin_status(address: str) -> str:
    url = f"https://api.pharosnetwork.xyz/sign/status?address={address}"
    try:
        res = requests.get(url, headers=headers)
        if res.ok:
            print("✅ Status check successful:", res.json())
            return res.json().get("data", {}).get("status", "")
        else:
            print(f"❌ Failed to check status: {res.status_code}")
    except Exception as e:
        print(f"❌ Error checking sign-in status: {e}")
    return ""


def perform_signin(address: str):
    url = f"https://api.pharosnetwork.xyz/sign/in?address={address}"
    try:
        res = requests.get(url, headers=headers)
        if res.ok:
            print("✅ Sign-in successful:", res.json())
        else:
            print(f"❌ Sign-in failed: {res.status_code}")
    except Exception as e:
        print(f"❌ Error during sign-in: {e}")


def countdown(seconds):
    try:
        while seconds > 0:
            hrs, rem = divmod(seconds, 3600)
            mins, secs = divmod(rem, 60)
            print(f"\r⏳ Waiting {int(hrs):02}:{int(mins):02}:{int(secs):02}", end="")
            time.sleep(1)
            seconds -= 1
        print()
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user.")
        exit()


# 🔁 Infinite loop
while True:
    print("\n🔍 Checking daily sign-in status...")
    status = check_signin_status(sender_address)

    if status == "1111222":
        print("🟡 Not signed in yet. Attempting to sign in...")
        perform_signin(sender_address)
        print("⏲️ Waiting 24 hours until next check.")
        countdown(86400)  # 24 hours

    elif status == "1111022":
        print("🟢 Already signed in today.")
        print("⏲️ Will check again in 2 hours.")
        countdown(7200)  # 2 hours

    else:
        print(f"⚠️ Unknown status: {status}. Retrying in 5 minutes.")
        countdown(300)  # 5 minutes
