// SPDX-License-Identifier: MIT
pragma solidity ^0.8.8;

import "./PriceConverter.sol";

error NotOwner();

contract FundMe {
    using PriceConverter for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    // Could we make this constant?  /* hint: no! We should make it immutable! */
    address public immutable i_owner;
    uint256 public constant MINIMUM_USD = 50 * 10 ** 18;

    constructor() {
        i_owner = msg.sender;
    }

    function fund() public payable {
        require(msg.value.getConversionRate() >= MINIMUM_USD, "You need to spend more ETH!");
        // require(PriceConverter.getConversionRate(msg.value) >= MINIMUM_USD, "You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public onlyOwnerFunction {
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0; // reset funder amount  

        }

        // reset funders array and withdraw the funds
        funders = new address[](0);

        // msg.sender = address
        // payable(msg.sender) ---> typecast to payable address

        //transfer ---> failed => revert()
        // payable(transfer(msg.sender, address(this).balance));

        // //send ---> failed => boolean
        // bool sendSuccess =payable(msg.sender).send(address(this).balance);
        // require(sendSuccess, "Send failed");
        
        // call --> low level
        (bool callSuccess, )= payable(msg.sender).call{value: address(this).balance}("");
        require(callSuccess, "Call failed");
    }

    modifier onlyOwnerFunction {
        
        if(msg.sender != i_owner) {
            revert NotOwner();
        }

        _; // continue the function ---> notice after require
    }

    receive() external payable {
        fund();
    }

    fallback() external payable {
        fund();
    }

}
