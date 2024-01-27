import json

from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
load_dotenv()

def read_DATA():
    w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
    # my_address = os.getenv("WALLET")
    # private_key = os.getenv("WALLET_PASSWORD")
    with open("blockchain_backend/workingcode/address.json","r") as file:
        contract1=json.loads(file.read())

    with open("blockchain_backend/workingcode/Abi.json","r") as file:
        abi1=file.read()
    abiContract=json.loads(abi1)
    recordsContract = w3.eth.contract(address=contract1["address"], abi=abiContract)
    Table_data=(recordsContract.functions.getAllRecordItems().call())
    # print(Table_data)
    return Table_data


blockchainData=read_DATA()
# print(blockchainData)
def transaction(userID,AdminID):
    w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
    my_address = os.getenv("WALLET")
    private_key = os.getenv("WALLET_PASSWORD")
    address1=str(userID)
    address2=str(AdminID)
    with open("blockchain_backend/workingcode/address.json","r") as file:
     contract1=json.loads(file.read())
    with open("blockchain_backend/workingcode/Abi.json","r") as file:
     abi1=file.read()
    abiContract=json.loads(abi1)
    recordsContract = w3.eth.contract(address=contract1["address"], abi=abiContract)
    with open("blockchain_backend/workingcode/nonce.json","r") as file:
     nonce1=json.loads(file.read())
    nonce=int(nonce1["nonce"])
    with open("blockchain_backend/workingcode/nonce.json","w") as file:
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
    greeting_transaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    return tx_receipt
    

    