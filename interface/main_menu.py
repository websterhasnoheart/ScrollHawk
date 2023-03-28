import os
import sys
from pyfiglet import Figlet
from pathlib import Path
from .zkSync_menu import zk_main_menu
from .scroll_menu import scroll_main_menu
from .stark_menu import stark_main_menu
from utils.wallets import wallet_list, display_data
from utils.gas_price import get_gas_prices

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
abs_path = str(path.parent.absolute())
sys.path.append(abs_path)


def main_menu():
    f = Figlet(font='slant')
    os.system("clear")
    print(f.renderText('ScrollHawk'))
    base_fee, priority_fee = get_gas_prices()
    print(f'Current gas fee: {base_fee} gwei | Priority fee {priority_fee} gwei')
    print("""
[1] Modules
[2] Config settings
[3] Wallet info
        """)
    option = input("\ninput option: ")
    if option == '1':
        modules_menu()
    elif option == '2':
        config_menu()
    elif option == '3':
        display_data(wallet_list())
        if os.name == "nt":  # For Windows systems
            os.system("pause")
        else:  # For Linux and macOS systems
            os.system("read -rsp $'Press any key to go back:\\n' -n 1 key")
            os.system("clear")
            main_menu()
    else:
        print("Invalid inut")
        main_menu()


def modules_menu():
    f = Figlet(font='slant')
    os.system("clear")
    print(f.renderText('ScrollHawk'))
    print("choose a module and start grinding: ")
    print("""
[1] zkSync
[2] Starknet
[3] layerZero
[4] Back
        """)
    option = input("\nYour option: ")
    if option == '1':
        zk_main_menu()
    elif option == '2':
        stark_main_menu()
    elif option == '3':
        scroll_main_menu()
    elif option == '4':
        main_menu()
    else:
        print("Invalid inut")
        modules_menu()


def config_menu():
    pass
