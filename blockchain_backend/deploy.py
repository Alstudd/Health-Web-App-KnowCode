from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()
with open("./abi.json","r") as file:
    abi1=file.read()
with open("./bytecode.json","r") as file:
    bytecode1=file.read()
import json

BytecodeContract=json.loads(bytecode1)
abiContract=json.loads(abi1)

# w3 = Web3.HTTPProvider(os.getenv("HTTP_URL"))
w3=Web3(Web3.HTTPProvider(os.getenv("HTTP_URL")))
walletAddress=os.getenv("WALLET")
walletPrivateKey=os.getenv("WALLET_PASSWORD")
chain_id=11155111
recordsContract=w3.eth.contract(abi=abiContract,bytecode=BytecodeContract)
print(recordsContract)

nonce=w3.eth.get_transaction_count(walletAddress)
transaction = recordsContract.constructor().build_transaction({"chainId":chain_id,"from":walletAddress,"nonce":nonce})
#signing the transaction

signedTxn=w3.eth.account.sign_transaction(transaction,private_key=walletPrivateKey)
# print(signedTxn)
TxnHashing=w3.eth.send_raw_transaction(signedTxn.rawTransaction)
print(f"Txn hash={TxnHashing}")
txn_receipt=w3.eth.wait_for_transaction_receipt(TxnHashing)
# print(txn_receipt)
print(f"contract address ={txn_receipt['contractAddress']} \n transaction hash= {w3.to_hex(txn_receipt['transactionHash'])} \n blockNumber={txn_receipt['blockNumber']}")

with open("ContractInfo.json","w") as file:
    json.dump({
        "ContractAddress":txn_receipt['contractAddress'],
        "TransactionHash":w3.to_hex(txn_receipt['transactionHash']),
        "blockNumber":txn_receipt['blockNumber']
    },file)