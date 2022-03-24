pragma solidity ^0.8.0;

// Basic smart contract that sets a value

contract MContract {
    uint256 number;

    constructor() public {
        number = 0;
    }

    function setNumber(uint256 _num) public {
        number = _num;
    }

    function getNumber() public view returns (uint256) {
        return number;
    }
}
