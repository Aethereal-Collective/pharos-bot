import random
import time
import requests
from web3 import Web3, Account

w3 = Web3(Web3.HTTPProvider("https://testnet.dplabs-internal.com"))

if not w3.is_connected():
    raise Exception("Gagal terhubung ke jaringan Pharos Testnet")

with open("pvt.txt", "r") as f:
    private_key = f.readline().strip()

account = Account.from_key(private_key)
sender_address = account.address

print(f"Alamat pengirim: {sender_address}")

with open("recipients.txt", "r") as f:
    recipient_addresses = [line.strip() for line in f if line.strip()]

# Input jumlah cycle
total_cycles = int(input("Masukkan jumlah cycle pengiriman: "))

nonce = w3.eth.get_transaction_count(sender_address)

with open("token.txt", "r") as f:
    bearer_token = f.readline().strip()
task_id = 103

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "authorization": f"Bearer {bearer_token}",
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

for i in range(total_cycles):
    chosen_address = random.choice(recipient_addresses)
    random_amount = round(random.uniform(0.001, 0.002), 6)
    amount_in_wei = w3.to_wei(random_amount, 'ether')

    tx = {
        'to': chosen_address,
        'value': amount_in_wei,
        'gas': 21000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': nonce + i,
        'chainId': 688688,
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_hash_hex = w3.to_hex(tx_hash)
    print(f"[Cycle {i+1}] Kirim {random_amount} PHRS ke {chosen_address} | TX Hash: {tx_hash_hex}")

    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        print(f"Transaksi confirmed di block {receipt.blockNumber}")

        url = (
            f"https://api.pharosnetwork.xyz/task/verify?"
            f"address={sender_address}&task_id={task_id}&tx_hash={tx_hash_hex}"
        )
        response = requests.post(url, headers=headers)
        if response.ok:
            print(f"Verifikasi berhasil: {response.json()}")
        else:
            print(f"Verifikasi gagal: {response.status_code} | {response.text}")

    except Exception as e:
        print(f"Error saat menunggu transaksi: {e}")

    if i < total_cycles - 1:
        time.sleep(30)
