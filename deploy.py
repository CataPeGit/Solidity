from solcx import compile_standard, install_solc
import json
import web3 from Web3
import os
from dotenv import load_dotenv

install_solc("0.6.0")

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#connecting to ganache
w3 = WEb3(Web3.HTTPProvider("http://0.0.0.0:8545"))
chain_id = 1337
my_address = "0x"
private_key = os.getenv("PRIVATE_KEY")

# creting the contract
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
#get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

#build transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId":chain_id, "from": my_address, "nonce": nonce})
#sign transcation
signed_txn = w3.eth.accont.sign_transaction(transaction, private_key = private_key)
#send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transcation_receipt(tx_hash)
print("Deployed!")

# working with the contract
# we need the address and the abi
simple_storage = w3.eth.contract(address = tx_receipt.contractAddress, abi = abi)

print(simple_storage.functions.retrieve().call())


store_transaction = simple_storage.functions.store(15).bulidTransaction(
    {
        "chainId":chain_id, "from" : my_address, "nonce": nonce + 1

    }
)
signed_store_txn = w3.eth.account.signed_transaction(
    store_transaction,private_key = private_key
)
print("Updating contract...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("updated!")

print(simple_storage.functions.retrieve().call())

























