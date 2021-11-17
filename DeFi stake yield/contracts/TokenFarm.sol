// SPDX-License-Identifier// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Owanable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// We want to stake tokens
// We want to unstake tokens
// We want to issue token rewards
// Allow tokens to be added and staked to out contract
// Get value of the staked tokens in the platform

contract TokenFarm is Ownable {
    // We use this mapping in order to keep track of how much each staker has staked
    // mapping token address -> staker address -> amount
    mapping(address => mapping(address => uint256)) public stakingBalance;

    // mapping each address to the number of tokens that it has staked
    mapping(address => uint256) public uniqueTokensStaked;

    // mapp address to token price feed
    mapping(address => address) public tokenPriceFeedMapping;

    // List of all stakers on the platform:
    address[] public stakers;

    // List of tokens allowed into staking
    address[] public allowedTokens;

    IERC20 public dappToken;

    // we need to know what reward token is there going to be from the start
    // in order to help us issue rewards
    constructor(address _dappTokenAddres) public {
        dappToken == IERC20(_dappTokenAddres);
    }

    function setPriceFeedContract(address _token, address _priceFeed)
        public
        OnlyOwner
    {
        // set price feed associated with a token
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function issueTokens() public onlyOwner {
        // --- We want to issue token rewards
        for (
            uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
            stakersIndex++
        ) {
            // grab one staker at the time
            address recipient = stakers[stakersIndex];
            uint256 userTotalValue = getUserTotalValue(recipient);

            // send them a token reward based on the total value locked
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        // returning the total value locked by the user
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No tokens staked!");

        for (
            uint256 allowedTokenIndex = 0;
            allowedTokenIndex < allowedTokens.length;
            allowedTokenIndex++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _user,
                    allowedTokens[allowedTokenIndex]
                );
        }

        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        // returns the value of how much the user staked of this single token
        // example: 1 ETH -> 4000$ , then returns 4000
        if (uniqueTokensStaked[_user] <= 0) {
            return 0; // we use return instead of require so that the transaction does not revert
        }

        // we need price of the token * stakingBalance[_token][user]
        (uint256 price, uint256 decimals) = getTokenValue(_token);

        // stakingBalance[token][user] -> amount staked by the user
        // price -> current price of the staked token
        return ((stakingBalance[_token][_user] * price) / 10**decimals);
    }

    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        // get value of the staked tokens in the platform
        // we will use the chainlink pricefeeds to get accurate token price data
        // we need a price feed address
        // we will map each token to their associated price feed addresses
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function stakeTokens(uint256 _amount, address _token) {
        // --- We want to stake tokens
        // What tokens can be staked? -- any token in the 'allowedTokens' list
        // How much can the user stake? -- any amount bigger than 0
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "Token is currently not allowed"); // checking if the token is allowed

        // now we will call a transferFrom function on ERC20
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        // update the number of staked tokens of the staker
        updateUniqueTokensStaked(msg.sender, _token);

        // update staker balance
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;

        // add staker to the list of all stakers if it is their first time staking
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) public {
        uint256 balance = stakeBalance[_token][msg.sender];
        require(balance > 0, "Staking balance cannot be 0");

        // transfer balance to msg.sender and set the new balance as 0
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;
    }

    function updateUniqueTokensStaked(address user, address token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner {
        // add a token to the list of allowed tokens
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        // looping trough the list of allowed tokens in order to check if the given token is there
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokenIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }
        return false;
    }
}
