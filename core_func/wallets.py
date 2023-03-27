import csv
from prettytable import PrettyTable
from dotenv import find_dotenv, load_dotenv
from web3 import Web3
import os

# Replace 'output.csv' with the desired name for your new CSV file.
CSV_FILE = './wallets_info.csv'
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")

def read_csv_file(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def display_data(data):
    table = PrettyTable()
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    # Add columns to the table.
    table.field_names = ["Index", "Wallet_Name", "Wallet_Address", "L1 Balance"]
    # Add rows to the table.
    for row in data:
        table.add_row([row["index"], row["name"], row["address"], get_eth_balance(w3, row["address"])])
    print(table)

def wallet_list():
    data = read_csv_file(CSV_FILE)
    display_data(data)
    return data

def get_eth_balance(w3, address):
    balance = w3.eth.getBalance(address)
    return round(w3.fromWei(balance, "ether"),3)

def select_wallet(index):
    data = wallet_list()
    return data[index]
