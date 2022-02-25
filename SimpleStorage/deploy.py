from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Compile our solidity code
# And save it into compiled_sol

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# dump the compiled code into a .json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]


# get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# Connecting to ganache

# RCP Server
w3 = Web3(Web3.HTTPProvider("#### INFURA LINK ####"))
# Chain id
chainId = 42
# Address to deploy from
my_address = "0x062fdB0a8E563e9B0450f339037b600D45FfB550"
# Private key (needed for signing transactions)
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the lastest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1 Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainId, "from": my_address, "nonce": nonce}
)
# 2 Signing the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract...")
# 3 Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# stop and wait for the transaction
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


print("Contract deployed!")

# Working with the contract
# we need the address of the contract and the abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")

# 1 Build a transaction
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chainId,
        "from": my_address,
        "nonce": nonce + 1,
        # we use nonce+1 because we already used nonce when creating the initial transaction
    }
)
# 2 Signing the transaction
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# 3 Send the signed transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# wait for the transaction to finish
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print("Contract updated!")
print(simple_storage.functions.retrieve().call())
