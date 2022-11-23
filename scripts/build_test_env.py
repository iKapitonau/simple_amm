from brownie import LiquidityPool, LiquidityPoolFactory, TokenA, TokenB, TokenC
from scripts.utils import get_deployer_account

def deploy_tokens():
    deployer = get_deployer_account()
    token_a = TokenA.deploy(deployer, 1000, {'from': deployer});
    token_b = TokenB.deploy(deployer, 3000, {'from': deployer});
    token_c = TokenC.deploy(deployer, 5000, {'from': deployer});
    return (token_a, token_b, token_c)

def deploy_liquidity_pool_factory():
    return LiquidityPoolFactory.deploy({'from': get_deployer_account()})

def deploy_liquidity_pool(token_a, token_b):
    return LiquidityPool.deploy(token_a, token_b, {'from': get_deployer_account()})

def main():
    token_a, token_b, token_c = deploy_tokens()
    print(f'TokenA at {token_a}, TokenB at {token_b}, TokenC at {token_c}')
    factory = deploy_liquidity_pool_factory()
    print(f'Factory at {factory}')
    liquidity_pool = deploy_liquidity_pool(factory, token_a, token_b)
    print(f'LiquidityPool of tokens {token_a} and {token_b} at {liquidity_pool}')

