// SPDX-License-Identifier: MIT

pragma solidity ^0.8.8;

contract SafeMathTester.sol {

    // prior to 0.8 solidity ints we're "unchecked" uint8 e = 255+1 = 0 ;!!!
    // overflow/underflow on variable
    uint8 public bigNumber = 255;

    function add() public {
        unchecked {bigNumber = bigNumber + 1;}
    }

}