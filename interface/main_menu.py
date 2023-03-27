import os
import sys
from pyfiglet import Figlet
from pathlib import Path
from .zkSync_menu import zk_main_menu
from .scroll_menu import scroll_main_menu
from .stark_menu import stark_main_menu
from core_func.wallets import wallet_list

myDir = os.getcwd()
sys.path.append(myDir)
path = Path(myDir)
abs_path = str(path.parent.absolute())
sys.path.append(abs_path)

def main_menu():
    f = Figlet(font = 'slant')
    os.system("clear")
    print (f.renderText('ScrollHawk'))
    print("Welcome to ScrollHawk\n")
    print("choose an option")
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
        wallet_list()
        if os.name == "nt":  # For Windows systems
            os.system("pause")
        else:  # For Linux and macOS systems
            os.system("read -rsp $'Press any key to go back:\\n' -n 1 key")
            main_menu()
    else:
        print("Invalid inut")
        main_menu()

def modules_menu():
    f = Figlet(font = 'slant')
    os.system("clear")
    print (f.renderText('ScrollHawk'))
    print("\nchoose a module and start grinding: \n")
    print("""
[1] zkSync
[2] Starknet
[3] Scroll
        """)
    option = input("\nYour option: ")
    if option == '1':
        zk_main_menu()
    elif option == '2':
        stark_main_menu()
    elif option == '3':
        scroll_main_menu()
    else:
        print("Invalid inut")
        modules_menu()


def config_menu():
    pass
