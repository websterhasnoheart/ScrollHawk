from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.manage_contracts.gas_provider import StaticGasProvider
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import Token
from zksync2.provider.eth_provider import EthereumProvider
import os
from dotenv import find_dotenv, load_dotenv


dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
ETH_NODE_URL = os.getenv("ETH_NODE_URL")
ZKSYNC_NETWORK_URL = "https://zksync2-testnet.zksync.dev"

def deposit(private_key, eth, gas_price, priority_fee, gas_limit):
    eth_web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
    eth_web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    zksync_web3 = ZkSyncBuilder.build(ZKSYNC_NETWORK_URL)
    account: LocalAccount = Account.from_key(private_key)
    gas_provider = StaticGasProvider(eth_web3.toWei(gas_price, "gwei"), gas_limit)
    eth_provider = EthereumProvider.build_ethereum_provider(zksync=zksync_web3,
                                                            eth=eth_web3,
                                                            account=account,
                                                            gas_provider=gas_provider)
    tx_receipt = eth_provider.deposit(Token.create_eth(),
                                      eth_web3.toWei(eth, "ether"),
                                      account.address,
                                      priority_fee=eth_web3.toWei(priority_fee, "gwei"))
    print(f"tx status: {tx_receipt['status']}")
