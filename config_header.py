from login import get_bearer_token

# Get token once when loading config
BEARER_TOKEN = get_bearer_token()

# === Headers ===
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "authorization": f"Bearer {BEARER_TOKEN}",
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