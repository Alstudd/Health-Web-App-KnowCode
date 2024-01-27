import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware

load_dotenv()


with open("./recordsContracts.sol", "r") as file:
    recordsStorage = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.22")

# Solidity source code
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
    solc_version="0.8.22",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["Records"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
chain_id = 11155111

if chain_id == 4:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(w3.clientVersion)
#Added print statement to ensure connection suceeded as per
#https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority

my_address = os.getenv("WALLET")
private_key = os.getenv("WALLET_PASSWORD")
# my_address = "0xdEe5B56dc9BBafBA12586E0904F61B5A1d01ba0c"
# private_key = "a221652ac7a797a809e75ac73467ef0375727e2ea22a6e6659d55feaead6b77e"
    
# my_address = "0x440d56aa3C1e18A9Df0B1fff87949B3799EE501a"
# private_key = "8669a8ea8132cbb981e5aa3fb1e3ecba29ad221c2903475e50512f9b2e580cf5"


# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


address1=str(222)
address2=str(111)
# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
print(simple_storage.functions.getAllRecordItems().call())
greeting_transaction = simple_storage.functions.addItem(address1,address2).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
print(tx_receipt)

print(simple_storage.functions.getAllRecordItems().call())