import requests
import json


def get_contract_abi(contract_address):
    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={ETHERSCAN_API}"
    response = requests.get(url)
    response_data = json.loads(response.text)

    if response_data["status"] == "1":
        contract_abi = json.loads(response_data["result"])
        return contract_abi
    else:
        print("Error:", response_data["message"])
        