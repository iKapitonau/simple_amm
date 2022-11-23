from brownie import LiquidityPool, LiquidityPoolFactory, TokenA, TokenB, TokenC
from scripts.build_test_env import *
import pytest

def test_liquidity_factory_creates_pool():
    token_a, token_b, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    liquidity_pool = factory.createPool(token_a, token_b)
    assert factory.liquidityPools(token_a, token_b) == liquidity_pool.return_value

def test_liquidity_factory_fails_on_duplicates_1():
    token_a, token_b, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    liquidity_pool = factory.createPool(token_a, token_b)
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(token_a, token_b)

def test_liquidity_factory_fails_on_duplicates_2():
    token_a, token_b, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    liquidity_pool = factory.createPool(token_a, token_b)
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(token_b, token_a)

def test_liquidity_factory_fails_on_same_tokens():
    token_a, _, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(token_a, token_a)

def test_liquidity_factory_fails_on_empty_tokens_1():
    token_a, _, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(0, token_a)

def test_liquidity_factory_fails_on_empty_tokens_2():
    token_a, _, _ = deploy_tokens()
    factory = deploy_liquidity_pool_factory()
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(token_a, 0)

def test_liquidity_factory_fails_on_empty_tokens_3():
    factory = deploy_liquidity_pool_factory()
    with pytest.raises(Exception):
        liquidity_pool = factory.createPool(0, 0)
