# config.py
from web3 import Web3, Account
from eth_account.messages import encode_defunct


# === Web3 Setup ===
w3 = Web3(Web3.HTTPProvider("https://testnet.dplabs-internal.com"))
if not w3.is_connected():
    raise Exception("Failed to connect to Pharos Testnet")

# === Private Key & Account ===
with open("pvt.txt", "r") as f:
    private_key = f.readline().strip()

account = Account.from_key(private_key)
sender_address = account.address

# === Recipients ===
with open("recipients.txt", "r") as f:
    recipient_addresses = [line.strip() for line in f if line.strip()]



