import os
import sys
from pyfiglet import Figlet
from pathlib import Path
from utils.wallets import wallet_list, display_data
from utils.gas_price import get_gas_prices
import time
from core_func.starkNet.basic_func import starkNet_deposit


myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
abs_path = str(path.parent.absolute())
sys.path.append(abs_path)
gas_limit = 500000


def stark_main_menu():
    f = Figlet(font='standard', width=160)
    os.system("clear")
    print(f.renderText('z k S y n c'))
    print("Select an interaction activity: ")
    print("""
[1] StarkNet Bridge Deposit
[2] Orbiter Bridge Deposit
[3] Bridge Swap
[4] StarkNet Bridge Withdrawal
[5] Orbiter Bridge Withdrawal
        """)
    option = input("\nChoose your option: ")
    if option == '1':
        wallet_data = wallet_list()
        display_data(wallet_data)
        print("Select a wallet to deposit funds \n")
        wallet_index = int(input("Input by index: "))
        eth_amount = float(input("Amount to deposit: "))
        expected_gas = int(input("Input your expected gas price: "))

        while True:
            gas_price, priority_fee = get_gas_prices()
            if expected_gas >= gas_price:
                break
            else:
                print(
                    f"Current gas price ({gas_price} Gwei) is higher than expected gas price ({expected_gas} Gwei). Waiting for gas price to decrease...")
                time.sleep(120)
        private_key = wallet_data[wallet_index]["privatekey"]
        wallet_address = wallet_data[wallet_index]["address"]
        wallet_name = wallet_data[wallet_index]["name"]
        to_address = wallet_data[wallet_index]["argentWallet"]
        starkNet_deposit(private_key, wallet_address, to_address,
                         eth_amount, gas_price, priority_fee, gas_limit)
        if os.name == "nt":  # For Windows systems
            os.system("pause")
        else:  # For Linux and macOS systems
            os.system("read -rsp $'Press any key to go back:\\n' -n 1 key")
            stark_main_menu()
