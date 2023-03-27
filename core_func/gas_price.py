import os
import time
from web3 import Web3
from dotenv import find_dotenv, load_dotenv


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
POLL_INTERVAL_SECONDS = 10  # Adjust this value to set the polling interval.

def get_gas_prices():
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))

    # Obtain the current base fee and priority fee (tip) in Gwei.
    block = w3.eth.getBlock("latest")
    base_fee = round(block["baseFeePerGas"] / 1e9,2)
    priority_fee = round(w3.eth.max_priority_fee / 1e9,2)

    return base_fee, priority_fee

def gas_oclock():
    print("Monitoring Ethereum gas prices...")

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        try:
            base_fee, priority_fee = get_gas_prices()
            print(f"Base fee: {base_fee} Gwei | Priority fee: {priority_fee} Gwei")
        except Exception as e:
            print(f"Error fetching gas prices: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)
