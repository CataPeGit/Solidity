from scripts.helpful_scripts import get_account
from brownie import Collectible

# !!! Add IPFS companion extension to your browser if you can't see the token URI !!!
sample_token_URI = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

"""
def deploy_and_create():
    account = get_account()
    collectible = Collectible.deploy({"from": account})
    transaction = collectible.createCollectible(sample_token_URI, {"from": account})
    transaction.wait(1)
    print(
        f"See your NFT: {OPENSEA_URL.format(collectible.address, collectible.tokenCounter - 1)}"
    )
    return collectible
"""


def deploy_and_create():
    account = get_account()
    collectible_contract = Collectible.deploy({"from": account})
    tx = collectible_contract.createCollectible(sample_token_URI, {"from": account})
    tx.wait(1)
    print(
        f"See your NFT:  {OPENSEA_URL.format(collectible_contract.address, collectible_contract.tokenCounter() - 1)}"
    )
    return collectible_contract


def main():
    deploy_and_create()
