from brownie import LiquidityPool, LiquidityPoolFactory, TokenA, TokenB, TokenC, accounts
from scripts.build_test_env import *
import pytest
import math

def test_adding_liquidity():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})

    assert liquidity_pool.balance1() == 100 and \
        liquidity_pool.balance2() == 100 and \
        balance1_before - 100 == token_a.balanceOf(deployer) and \
        balance2_before - 100 == token_b.balanceOf(deployer) and \
        liquidity_pool.shares(deployer) == 100 and \
        liquidity_pool.totalShares() == 100

def test_adding_liquidity_with_no_tokens():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    account = accounts[1]
    amount1, amount2 = (100, 100)
    with pytest.raises(Exception):
        liquidity_pool.addLiquidity(amount1, amount2, {'from': account})

def test_adding_liquidity_with_zero_amounts():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (0, 0)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    with pytest.raises(Exception):
        liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})

def test_adding_liquidity_with_wrong_amounts():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    amount1, amount2 = (30, 70)
    with pytest.raises(Exception):
        liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})

def test_removing_full_liquidity():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    liquidity_pool.removeLiquidity(liquidity_pool.shares(deployer), {'from': deployer})
    assert liquidity_pool.balance1() == 0 and \
        liquidity_pool.balance2() == 0 and \
        balance1_before == token_a.balanceOf(deployer) and \
        balance2_before == token_b.balanceOf(deployer) and \
        liquidity_pool.shares(deployer) == 0 and \
        liquidity_pool.totalShares() == 0

def test_removing_zero_liquidity():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    with pytest.raises(Exception):
        liquidity_pool.removeLiquidity(0, {'from': deployer})

def test_removing_part_of_liquidity():
    token_a, token_b, _ = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    liquidity_pool.removeLiquidity(50, {'from': deployer})
    assert liquidity_pool.balance1() == 50 and \
        liquidity_pool.balance2() == 50 and \
        balance1_before - 50 == token_a.balanceOf(deployer) and \
        balance2_before - 50 == token_b.balanceOf(deployer) and \
        liquidity_pool.shares(deployer) == 50 and \
        liquidity_pool.totalShares() == 50

def test_swap_with_wrong_token():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    with pytest.raises(Exception):
        liquidity_pool.swap(token_c, 20, {'from': deployer})

def test_swap_with_zero_amount():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    with pytest.raises(Exception):
        liquidity_pool.swap(token_a, 0, {'from': deployer})

def test_swap_with_huge_amount():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    with pytest.raises(Exception):
        liquidity_pool.swap(token_a, 10000, {'from': deployer})

def test_swap_with_sufficient_amount():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    liquidity_pool.swap(token_a, 30, {'from': deployer})
    assert liquidity_pool.balance1() == 130 and \
        liquidity_pool.balance2() == 78 and \
        balance1_before - 100 - 30 == token_a.balanceOf(deployer) and \
        balance2_before - 100 + 22 == token_b.balanceOf(deployer)

def test_swap_with_removing_liquidity():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    amount1, amount2 = (100, 100)
    balance1_before = token_a.balanceOf(deployer)
    balance2_before = token_b.balanceOf(deployer)
    token_a.approve(liquidity_pool, balance1_before, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before, {'from': deployer})
    liquidity_pool.addLiquidity(amount1, amount2, {'from': deployer})
    liquidity_pool.swap(token_a, 30, {'from': deployer})
    liquidity_pool.removeLiquidity(liquidity_pool.shares(deployer), {'from': deployer})
    assert liquidity_pool.balance1() == 0 and \
        liquidity_pool.balance2() == 0 and \
        balance1_before == token_a.balanceOf(deployer) and \
        balance2_before == token_b.balanceOf(deployer)

def test_removing_liquidity_with_two_lps():
    token_a, token_b, token_c = deploy_tokens()
    liquidity_pool = deploy_liquidity_pool(token_a, token_b)
    deployer = get_deployer_account()
    account = accounts[1]
    token_a.mint(account, 200)
    token_b.mint(account, 200)
    amount1_deployer, amount2_deployer = (100, 100)
    amount1_acc, amount2_acc = (200, 200)
    balance1_before_deployer = token_a.balanceOf(deployer)
    balance2_before_deployer = token_b.balanceOf(deployer)
    balance1_before_acc = token_a.balanceOf(account)
    balance2_before_acc = token_b.balanceOf(account)
    token_a.approve(liquidity_pool, balance1_before_deployer, {'from': deployer})
    token_b.approve(liquidity_pool, balance2_before_deployer, {'from': deployer})
    token_a.approve(liquidity_pool, balance1_before_acc, {'from': account})
    token_b.approve(liquidity_pool, balance2_before_acc, {'from': account})
    liquidity_pool.addLiquidity(amount1_deployer, amount2_deployer, {'from': deployer})
    liquidity_pool.addLiquidity(amount1_acc, amount2_acc, {'from': account})
    liquidity_pool.swap(token_a, 30, {'from': deployer})
    liquidity_pool.removeLiquidity(liquidity_pool.shares(deployer), {'from': deployer})
    assert liquidity_pool.balance1() == math.ceil((300 + 30) * 2 / 3) and \
        liquidity_pool.balance2() == math.ceil((300 - 26) * 2 / 3)  and \
        balance1_before_deployer - math.ceil(100 + 30 - (300 + 30) // 3) == token_a.balanceOf(deployer) and \
        balance2_before_deployer - math.ceil(100 - 26 - (300 - 26) // 3) == token_b.balanceOf(deployer)

