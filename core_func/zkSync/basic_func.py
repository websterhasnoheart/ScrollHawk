from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.manage_contracts.gas_provider import StaticGasProvider
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import Token, EthBlockParams
from zksync2.provider.eth_provider import EthereumProvider
import os
from dotenv import find_dotenv, load_dotenv
from zksync2.transaction.transaction712 import TxFunctionCall
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from eth_typing import HexStr
from zksync2.core.types import ZkBlockParams


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
ZKSYNC_NETWORK_URL = os.getenv("ZKSYNC_NETWORK_URL")


def deposit(private_key, eth, gas_price, priority_fee, gas_limit):
    eth_web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    eth_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    zksync_web3 = ZkSyncBuilder.build(ZKSYNC_NETWORK_URL)
    account: LocalAccount = Account.from_key(private_key)
    gas_provider = StaticGasProvider(
        eth_web3.toWei(gas_price, "gwei"), gas_limit)
    eth_provider = EthereumProvider.build_ethereum_provider(zksync=zksync_web3,
                                                            eth=eth_web3,
                                                            account=account,
                                                            gas_provider=gas_provider)
    tx_receipt = eth_provider.deposit(Token.create_eth(),
                                      eth_web3.toWei(eth, "ether"),
                                      account.address,
                                      priority_fee=eth_web3.toWei(priority_fee, "gwei"))
    print(f"tx status: {tx_receipt['status']}")


def check_balance(private_key):
    w3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    account: LocalAccount = Account.from_key(private_key)
    zksync_web3 = ZkSyncBuilder.build(ZKSYNC_NETWORK_URL)
    zk_balance = zksync_web3.zksync.get_balance(
        account.address, EthBlockParams.LATEST.value)
    return round(w3.fromWei(zk_balance, "ether"), 3)


def transfer_funds(private_key, eth, to_address, gas_price, priority_fee, gas_limit):
    eth_web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    amount = eth
    account: LocalAccount = Account.from_key(private_key)
    zksync_web3 = ZkSyncBuilder.build(ZKSYNC_NETWORK_URL)
    chain_id = zksync_web3.zksync.chain_id
    signer = PrivateKeyEthSigner(account, chain_id)

    nonce = zksync_web3.zksync.get_transaction_count(
        account.address, ZkBlockParams.COMMITTED.value)
    gas_price = zksync_web3.zksync.gas_price

    tx_func_call = TxFunctionCall(chain_id=chain_id,
                                  nonce=nonce,
                                  from_=account.address,
                                  to=to_address,
                                  value=Web3.toWei(amount, 'ether'),
                                  data=HexStr("0x"),
                                  gas_limit=gas_limit,  # unknown at this state, will be replaced by estimate_gas
                                  gas_price=gas_price,
                                  max_priority_fee_per_gas=eth_web3.toWei(priority_fee, "gwei"))
    estimate_gas = zksync_web3.zksync.eth_estimate_gas(tx_func_call.tx)
    print(f"Fee for transaction is: {estimate_gas * gas_price}")

    tx_712 = tx_func_call.tx712(estimate_gas)

    singed_message = signer.sign_typed_data(tx_712.to_eip712_struct())
    msg = tx_712.encode(singed_message)
    tx_hash = zksync_web3.zksync.send_raw_transaction(msg)
    tx_receipt = zksync_web3.zksync.wait_for_transaction_receipt(
        tx_hash, timeout=240, poll_latency=0.5)
    print(f"tx_hash : {tx_hash.hex()}, status: {tx_receipt['status']}")
