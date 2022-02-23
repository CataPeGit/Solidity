// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
        
    mapping(address => uint256) public addressToAmmountFunded;    
    address[] public funders;
    address public owner;
    
    constructor() public{
        owner = msg.sender; //whoever deploys the smart contract will be the owner
    }
    
    function fund() public payable {
        uint256 minimumUSD= 50 * (10 ** 18);
        require(getConversionRate(msg.value) >= minimumUSD , "More Eth required for the transaction!");
        
        addressToAmmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns (uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x####################...); //Kovan Testnet: 0x9326BFA02ADD2366b30bacB125260Af641031331 
        return priceFeed.version();
    }
    
    function getPrice() public view returns (uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x####################...); //Kovan Testnet: 0x9326BFA02ADD2366b30bacB125260Af641031331 
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }
    
    function getConversionRate(uint256 ethAmount) public view returns(uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / (10 ** 18);
        return ethAmountInUsd;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _; // the rest of the function will go here
    }
    
    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance); // transfering "balance" amount of eth to "msg.sender"(meaning who called the function) from "address(this)"
        
        for (uint256 funderIndex = 0; funderIndex <= funders.length; funderIndex++)
            {
                address funder = funders[funderIndex];
                addressToAmmountFunded[funder] = 0;
            }
        funders = new address[](0);
    }
    
} 
    
