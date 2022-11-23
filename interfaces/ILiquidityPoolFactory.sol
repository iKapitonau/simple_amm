// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ILiquidityPoolFactory {
    function createPool(
        address _token1,
        address _token2
    ) external returns (address);
}
