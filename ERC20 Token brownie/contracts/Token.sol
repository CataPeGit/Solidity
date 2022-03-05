// contracts/Token.sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract _Token is ERC20 {
    // in wei
    constructor(uint256 initialSupply) ERC20("_Token", "OT") {
        _mint(msg.sender, initialSupply);
    }
}
