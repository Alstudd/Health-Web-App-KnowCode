import json

from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
my_address = os.getenv("WALLET")
private_key = os.getenv("WALLET_PASSWORD")
address1=str(22233)
address2=str(111555)
with open("./address.json","r") as file:
    contract1=json.loads(file.read())


# contractInfo=json.loads(contract1)
with open("./Abi.json","r") as file:
    abi1=file.read()
abiContract=json.loads(abi1)
recordsContract = w3.eth.contract(address=contract1["address"], abi=abiContract)
print(recordsContract.functions.getAllRecordItems().call())
with open("./nonce.json","r") as file:
    nonce1=json.loads(file.read())
nonce=int(nonce1["nonce"])

with open("./nonce.json","w") as file:
    json.dump({"nonce":nonce+1}, file)

greeting_transaction = recordsContract.functions.addItem(address1,address2).build_transaction(
    {
        "chainId": 11155111,
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
print(recordsContract.functions.getAllRecordItems().call())

