from web3 import Web3
import os
import json
from dotenv import load_dotenv
load_dotenv()
with open("./ContractInfo.json","r") as file:
    contract1=file.read()
contractInfo=json.loads(contract1)
with open("./abi.json","r") as file:
    abi1=file.read()
abiContract=json.loads(abi1)
w3=Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
walletAddress=os.getenv("WALLET")
walletPrivateKey=os.getenv("WALLET_PASSWORD")
chain_id=11155111

recordsContract=w3.eth.contract(address=contractInfo["ContractAddress"],abi=abiContract)
nonce=w3.eth.get_transaction_count(walletAddress)
print(f"Nonce:{nonce}")
# Calling the earlier values


# print(recordsContract.functions.getAllRecordItems().call({"from":walletAddress}))


gas_price_gwei=5000
address1=str(1111111)
address2=str(2222222)
store_Data_in_Blockchain=recordsContract.functions.addItem(address1,address2).build_transaction({
    "chainId":chain_id,"from":walletAddress,"nonce":nonce + 102,"gas_price": w3.to_wei(gas_price_gwei, 'gwei')
})
print(f"Stored request=\n{store_Data_in_Blockchain}")



#signing the transaction that I have made because function joh state 
#change krega have to make trnsaction and we have to sign that transaction



signed_store_Data_Txn=w3.eth.account.sign_transaction(
    store_Data_in_Blockchain,private_key=walletPrivateKey
)
print(f"stored signing=\n{signed_store_Data_Txn}")


#here we are hashing the transaction


stored_data_hashing=w3.eth.send_raw_transaction(signed_store_Data_Txn.rawTransaction)
print(f"storing the hash = \n{w3.to_hex(stored_data_hashing)}")
stored_data_txn_receipt=w3.eth.wait_for_transaction_receipt(stored_data_hashing)
print(f"txn receipt= \n{stored_data_txn_receipt}")

