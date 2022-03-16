from ctypes import addressof
from brownie import interface, config, network
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    # we will be working with LendingPool Aave contract
    # therefore we need the ABI and the address
    lending_pool = get_lending_pool()

    # approve sending ERC20 token
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    # now we can deposit
    transaction = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    transaction.wait(1)
    print("Deposited!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

    print("Let's borrow some DAI")
    # DAI in terms of ETH
    dai_to_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # we convert borrowable_eth to borrowable_dai * 95%
    # *95% because we don't want to get liquidated
    # the lower this percentage(such as 95%) the lower the risk
    amount_dai_to_borrow = (1 / dai_to_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow}")

    # Now we will borrow some DAI:
    # !!! for testnets you should make sure the LendingPool address is not updated !!!

    dai_address = config["networks"][network.show_active()]["dai_address"]

    # interest rate mode: 1->stable, 2->variable
    rate_mode = 1  # we use 1 for stable here

    borrow_transaction = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        rate_mode,
        0,
        account.address,
        {"from": account},
    )
    borrow_transaction.wait(1)
    print("DAI borrowed!")
    get_borrowable_data(lending_pool, account)

    # now that we borrowed we shall repay
    repay_all(amount, lending_pool, account, rate_mode)
    print("You just deposited, borrowed and repayed with Aave, Brownie and Chainlink")


def repay_all(amount, lending_pool, account, rate_mode):
    # we approve the erc20
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_address"],
        account,
    )
    # approve_erc20 already calls wait
    repay_transaction = lending_pool.repay(
        config["networks"][network.show_active()]["dai_address"],
        amount,
        rate_mode,
        account.address,
        {"from": account},
    )
    repay_transaction.wait(1)
    print("Repayed!")


def get_asset_price(price_feed_address):
    # we pass the address of asset to asset price feed contract
    # DAI to ETH in our case
    # using chainlink price feeds
    # as usual we need to grab the ABI and the address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI to ETH price is : {converted_latest_price}")
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"Amount of ETH deposited: {total_collateral_eth}")
    print(f"Amount of ETH borrowed: {total_debt_eth}")
    print(f"Amount of ETH you can borrow: {available_borrow_eth}")
    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 Token...")
    erc20 = interface.ERC20(erc20_address)
    transaction = erc20.approve(spender, amount, {"from": account})
    transaction.wait(1)
    print("Approved!")
    return transaction


def get_lending_pool():
    # we will get the right contract using the address provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
