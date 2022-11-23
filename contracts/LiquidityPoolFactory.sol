// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

import "./LiquidityPool.sol";

contract LiquidityPoolFactory is Ownable {
    mapping(address => mapping(address => address)) public liquidityPools;

    function createPool(address _token1, address _token2) public onlyOwner {
        // make tokens ordered
        if (_token1 > _token2) {
            (_token1, _token2) = (_token2, _token1);
        }
        require(
            liquidityPools[_token1][_token2] != address(0),
            "The pool already exists."
        );
        require(_token1 != _token2, "Equal tokens are not allowed.");
        LiquidityPool liquidityPool = new LiquidityPool(_token1, _token2);
        liquidityPools[_token1][_token2] = address(liquidityPool);
    }
}
