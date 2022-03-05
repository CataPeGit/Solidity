from brownie import _Token
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def deploy_Erc20():
    account = get_account()
    erc20 = _Token.deploy(initial_supply, {"from": account})
    print("Token deployed:")
    print(erc20.name())


def main():
    deploy_Erc20()
