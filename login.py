from eth_account.messages import encode_defunct

import json
import os
import time
import requests
import base64

from config import (
    w3,
    sender_address,
    private_key,
)

TOKEN_FILE = "token.txt"

LOGIN_MESSAGE = "pharos"

LOGIN_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-length": "0",
    "dnt": "1",
    "origin": "https://testnet.pharosnetwork.xyz",
    "priority": "u=1, i",
    "referer": "https://testnet.pharosnetwork.xyz/",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
}


def is_token_valid(token: str) -> bool:
    try:
        payload_encoded = token.split(".")[1]
        padding = "=" * (4 - len(payload_encoded) % 4)
        payload_encoded += padding

        payload_bytes = base64.urlsafe_b64decode(payload_encoded)
        payload = json.loads(payload_bytes)

        exp = payload.get("exp", 0)
        now = int(time.time())
        return now < exp
    except Exception as e:
        print("⚠️ Failed to check token validity:", e)
        return False


def load_token_from_file():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
            if token and is_token_valid(token):
                return token
    return None


def save_token_to_file(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def get_bearer_token():
    token = load_token_from_file()
    if token:
        print("ℹ️ Using token from local file")
        return token

    message_encoded = encode_defunct(text=LOGIN_MESSAGE)
    signed_message = w3.eth.account.sign_message(message_encoded, private_key=private_key)
    signature = w3.to_hex(signed_message.signature)

    login_url = f"https://api.pharosnetwork.xyz/user/login?address={sender_address}&signature={signature}"

    response = requests.post(login_url, headers=LOGIN_HEADERS)

    if response.ok:
        data = response.json()
        token = data.get("data", {}).get("jwt")
        if not token:
            raise Exception(f"Token not found in response: {data}")

        save_token_to_file(token)
        print("ℹ️ New token obtained and saved successfully")
        return token
    else:
        raise Exception(f"Login failed: {response.status_code} {response.text}")
