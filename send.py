import random
import time
import requests
from config import (
    w3,
    sender_address,
    private_key,
    recipient_addresses,
)

from config_header import headers

# Input jumlah cycle
total_cycles = int(input("Enter the number of sending cycles: "))
nonce = w3.eth.get_transaction_count(sender_address)

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
    print(f"[Cycle {i+1}] Sent {random_amount} PHRS to {chosen_address} | TX Hash: {tx_hash_hex}")

    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        print(f"Transaction confirmed in block {receipt.blockNumber}")

        url = (
            f"https://api.pharosnetwork.xyz/task/verify?"
            f"address={sender_address}&task_id={103}&tx_hash={tx_hash_hex}"
        )
        response = requests.post(url, headers=headers)
        if response.ok:
            print(f"✅ Verification success: {response.json()}")
        else:
            print(f"❌ Verification failed: {response.status_code} | {response.text}")

    except Exception as e:
        print(f"Error while waiting for transaction confirmation: {e}")

    if i < total_cycles - 1:
        time.sleep(30)
