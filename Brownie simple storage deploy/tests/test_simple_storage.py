from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange the test
    account = accounts[0]
    # Act on the test
    simple_storage = SimpleStorage.deploy({"from": account})
    first_stored_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert first_stored_value == expected


def test_updating_storage():
    # Arrange the test
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act on the test
    simple_storage.store(24, {"from": account})
    value_after_transaction = simple_storage.retrieve()
    expected = 24
    # Assert
    assert value_after_transaction == expected
