from web3 import Web3
import os
from dotenv import find_dotenv, load_dotenv
from eth_account import Account
# from utils.get_contract_info import get_contract_abi

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
STARKNET_BRIDGE_CONTRACT = os.getenv("STARKNET_BRIDGE_CONTRACT")
STARKNET_BRIDGE_PROXY_CONTRACT = os.getenv("STARKNET_BRIDGE_PROXY_CONTRACT")
ETHERSCAN_API = os.getenv("ETHERSCAN_API")

import requests
import json

# **************************** TO BE REMOVED ****************************
def get_contract_abi(contract_address):
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API}"
    response = requests.get(url)
    response_data = json.loads(response.text)

    if response_data["status"] == "1":
        contract_abi = json.loads(response_data["result"])
        return contract_abi
    else:
        print("Error:", response_data["message"])
# **********************************************************************

def starkNet_deposit(private_key, from_address, to_address, eth_amount, gas_price, priority_fee, gas_limit):
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    account = Account.from_key(private_key)
    abi = get_contract_abi(STARKNET_BRIDGE_CONTRACT)
    proxy_abi = get_contract_abi(STARKNET_BRIDGE_PROXY_CONTRACT)

    #Contract instances
    proxy_contract_instance = w3.eth.contract(address=STARKNET_BRIDGE_CONTRACT, abi=proxy_abi)

    #Units convert
    dec_address = int(to_address, 16)
    wei_amount = Web3.toWei(eth_amount, 'ether')

    # As there are 2 deposit() in the smart contract, prepare 2 groups of params
    function_name = "deposit"
    function_argument_types_1 = ("uint256")
    function_arguments_1 = (dec_address,)
    function_argument_types_2 = ("uint256, uint256")
    function_arguments_2 = (wei_amount,dec_address)

    transaction_data = proxy_contract_instance.functions[function_name](*function_arguments_1).buildTransaction({
        "from": from_address,
        "to" : to_address,
        "value" : eth_amount,
        "gas": gas_limit, # gas limit
        "gasPrice": gas_price, #base gas (wei)
        "maxPriorityFeePerGas" : priority_fee 
        "nonce": w3.eth.getTransactionCount(from_address),
    })

    
    # Sign and send the transaction if you have the private key
    signed_transaction = account.signTransaction(transaction_data, private_key)
    transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be confirmed
    transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

    if transaction_receipt["status"]:
        print(f"Transaction successful! Transaction hash: {transaction_hash.hex()}")
    else:
        print("Transaction failed.")

if __name__ == '__main__':
    private_key = '0xdfcd60210f90ed2494639bd29d9aaaf746d3093bb5f21e8e40e3924d12e46fc1'
    from_address = '0x0e552d0B3562806d1546B2f6b25cD973Ec65E4B9'
    to_address = '0x053B90D17b1F54dCe5A436C85B8c48724103a6e72e85734c8d7aEe461B5ac5c8'
    eth_amount = 0.01
    gas_price = 35
    priority_fee = 0.5
    gas_limit = 170000
    starkNet_deposit(private_key, from_address, to_address, eth_amount, gas_price, priority_fee, gas_limit)