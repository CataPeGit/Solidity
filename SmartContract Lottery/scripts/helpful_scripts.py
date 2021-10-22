from brownie import network, config, accounts, VRFCoordinatorMock, MockV3Aggregator, LinkToken, Contract

FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS or network.show_active() in FORKED_LOCAL_ENVIROMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config if defined,
    otherwise,it will deploy a mock version of that contract 
    and return that mock contract.

    Args:
        contract_name(string)
    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
        which would be MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        if len(contract_type) <= 0:
            # len(contract_type) is equal to MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1] -> we will grab the most recent deployment
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
        # MockV3Aggregator.abi
        return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

    print("Mock deployed!")
