// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/math/Math.sol";

contract LiquidityPool {
    address public immutable token1;
    address public immutable token2;
    uint public balance1;
    uint public balance2;
    uint public total_shares;
    mapping(address => uint256) shares;

    constructor(address _token1, address _token2) {
        require(_token1 != address(0) && _token2 != address(0) && _token1 != _token2);
        token1 = _token1;
        token2 = _token2;
    }

    function add_liquidity(uint256 _amount1, uint256 _amount2) external {
        require(_amount1 > 0 && _amount2 > 0);
        if (balance1 > 0 && balance2 > 0)
            require(balance1 * _amount2 == balance2 * _amount1, "x / y == dx / dy is not satisfied.");

        SafeERC20.safeTransferFrom(IERC20(token1), msg.sender, address(this), _amount1); 
        SafeERC20.safeTransferFrom(IERC20(token2), msg.sender, address(this), _amount2); 

        uint share = total_shares == 0 ?
            Math.sqrt(_amount1 * _amount2) :
            Math.min(
                total_shares * _amount1 / balance1,
                total_shares * _amount2 / balance2);

        balance1 += _amount1;
        balance2 += _amount2;
        total_shares += share;
        shares[msg.sender] += share;
    }

    function remove_liquidity(uint256 _share) external {
        require(_share > 0 && _share <= shares[msg.sender]);

        uint256 amount1 = _share * balance1 / total_shares;
        uint256 amount2 = _share * balance2 / total_shares;
        shares[msg.sender] -= _share;
        total_shares -= _share;
        balance1 -= amount1;
        balance2 -= amount2;

        SafeERC20.safeTransfer(IERC20(token1), msg.sender, amount1); 
        SafeERC20.safeTransfer(IERC20(token2), msg.sender, amount2); 
    }

    function swap(address _token, uint256 _amount) external {
        require(_amount > 0, "Amount must be positive.");
        require(_token == token1 || _token == token2, "No such token in the pool.");
        require(IERC20(_token).allowance(msg.sender, address(this)) >= _amount, "Not approved tokens.");

        // fee == 0.3%
        uint256 amount_after_fee = _amount * 997 / 1000;

        SafeERC20.safeTransferFrom(IERC20(_token), msg.sender, address(this), _amount);

        if (_token == token1) {
            uint256 amount_to_send = balance2 * amount_after_fee / (balance1 + amount_after_fee);
            balance1 += _amount;
            balance2 -= amount_to_send;
            SafeERC20.safeTransfer(IERC20(token2), msg.sender, amount_to_send);
        } else {
            uint256 amount_to_send = balance1 * amount_after_fee / (balance2 + amount_after_fee);
            balance2 += _amount;
            balance1 -= amount_to_send;
            SafeERC20.safeTransfer(IERC20(token1), msg.sender, amount_to_send);
        }
    }
}
