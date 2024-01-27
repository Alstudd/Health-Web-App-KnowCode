import json

from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
# from web3.middleware import geth_poa_middleware
load_dotenv()
with open("../recordsContracts.sol", "r") as file:
    recordsStorage = file.read()
print("Installing...")
install_solc("0.8.22")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": recordsStorage}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["evm"][
    "bytecode"
]["object"]

with open("bytecode.json", "w") as file:
    json.dump(bytecode, file)

with open("Abi.json", "w") as file:
    json.dump(compiled_sol, file)

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["metadata"]
)["output"]["abi"]

with open("Abi.json", "w") as file:
    json.dump(abi, file)

my_address = os.getenv("WALLET")
private_key = os.getenv("WALLET_PASSWORD")
w3=Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
chain_id=11155111
recordsContract=w3.eth.contract(abi=abi,bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)
print(f"type of nonce={type(nonce)}")
with open("nonce.json", "w") as file:
    json.dump({"nonce":nonce}, file)
transaction = recordsContract.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

with open("address.json", "w") as file:
    json.dump({"address":tx_receipt.contractAddress}, file)