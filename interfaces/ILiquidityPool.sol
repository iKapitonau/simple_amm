// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface ILiquidityPool {
    function addLiquidity(uint256 _amount1, uint256 _amount2) external;

    function removeLiquidity(uint256 _share) external;

    function swap(address _token, uint256 _amount) external;
}
