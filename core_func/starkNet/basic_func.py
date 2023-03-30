from web3 import Web3
import os
from dotenv import find_dotenv, load_dotenv
from eth_account import Account
from utils.get_contract_info import get_contract_abi

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
STARKNET_BRIDGE_CONTRACT = os.getenv("STARKNET_BRIDGE_CONTRACT")
STARKNET_BRIDGE_PROXY_CONTRACT = os.getenv("STARKNET_BRIDGE_PROXY_CONTRACT")
ETHERSCAN_API = os.getenv("ETHERSCAN_API")
STARKNET_CORE_CONTRACT = '0x739A654271c565839F0408546706bBea2F1FfE42'


def starkNet_deposit(private_key, from_address, to_address, eth_amount, gas_price, priority_fee, gas_limit, bridge_fee=0):
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    account = Account.from_key(private_key)
    abi = get_contract_abi(STARKNET_BRIDGE_CONTRACT)
    proxy_abi = get_contract_abi(STARKNET_BRIDGE_PROXY_CONTRACT)

    # Contract instances
    proxy_contract_instance = w3.eth.contract(
        address=STARKNET_BRIDGE_CONTRACT, abi=proxy_abi)

    # Units convert
    dec_address = int(to_address, 16)
    wei_amount = Web3.toWei(eth_amount, 'ether')
    eth_amount = Web3.toWei(eth_amount, 'ether')
    gas_price = Web3.toWei(gas_price, 'gwei')
    priority_fee = Web3.toWei(priority_fee, 'gwei')

    # As there are 2 deposit() in the smart contract, prepare 2 groups of params
    function_name = "deposit"
    # function_argument_types_1 = ("uint256")
    function_arguments_1 = (dec_address,)
    # function_argument_types_2 = ("uint256, uint256")
    function_arguments_2 = (wei_amount, dec_address)

    # Build transactions with customized bridge fee
    if bridge_fee == 0:
        transaction_data = proxy_contract_instance.functions[function_name](*function_arguments_1).buildTransaction({
            "from": from_address,
            "value": eth_amount,
            "gas": gas_limit,  # gas limit
            # base gas (wei), old gasPrice should not be used anymore
            "maxFeePerGas": gas_price,
            "maxPriorityFeePerGas": priority_fee,
            "nonce": w3.eth.getTransactionCount(from_address),
        })
    else:
        transaction_data = proxy_contract_instance.functions[function_name](*function_arguments_2).buildTransaction({
            "from": from_address,
            "value": eth_amount + float(bridge_fee),
            "gas": gas_limit,  # gas limit
            "maxFeePerGas": gas_price,  # base gas (wei)
            "maxPriorityFeePerGas": priority_fee,
            "nonce": w3.eth.getTransactionCount(from_address),
        })

    # Sign and send the transaction if you have the private key
    signed_transaction = account.signTransaction(transaction_data)
    transaction_hash = w3.eth.sendRawTransaction(
        signed_transaction.rawTransaction)

    # Wait for the transaction to be confirmed
    transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)

    if transaction_receipt["status"]:
        print(
            f"Transaction successful! Transaction hash: {transaction_hash.hex()}")
    else:
        print("Transaction failed.")


def orbiter_bridge_deposit():
    pass


if __name__ == '__main__':
    get_msg_fee()
