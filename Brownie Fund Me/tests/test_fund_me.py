from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIROMENTS, get_account
from scripts.deploy import deploy_fund_me
import pytest
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    # Arrange the contract
    account = get_account()
    fund_me = deploy_fund_me()
    # Act on the contract
    entrance_fee = fund_me.getEntranceFee() + 100
    transcation = fund_me.fund({"from": account, "value": entrance_fee})
    transcation.wait(1)
    # Assert
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing!")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
