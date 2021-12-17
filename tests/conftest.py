#!/usr/bin/python3

import pytest
import json
from collections import Counter, OrderedDict
from decimal import *
from MerkleTree import *
import brownie
from brownie import web3, accounts, Airdrop, ERC20

@pytest.fixture(scope="session")
def AirdropContract(ERC20Contract, merkle_tree):
    airdrop = Airdrop.deploy(ERC20Contract, merkle_tree.get_merkle_root(), accounts[3], {'from':accounts[0]})
    ERC20Contract.transfer(airdrop, 5 * 10 ** 6 * 10 ** 18)
    return airdrop

@pytest.fixture(scope="session")
def ERC20Contract():
    return ERC20.deploy("Test ERC20", "T20", {'from':accounts[1]})

@pytest.fixture(scope="session")
def reward_amounts():
    with open("somm_app_rewards.json") as openfile:
        somm_app_rewards = Counter(json.load(openfile))
        for key in somm_app_rewards:
            somm_app_rewards[key] = int(Decimal(str(somm_app_rewards[key])) * 10 ** 18)
    with open("uniswap_v3_pool_rewards.json") as openfile:
        uniswap_pool_rewards = Counter(json.load(openfile))
        for key in uniswap_pool_rewards:
            uniswap_pool_rewards[key] = int(Decimal(str(uniswap_pool_rewards[key])) * 10 ** 18)
    final_rewards = dict(uniswap_pool_rewards + somm_app_rewards)
    final_rewards = OrderedDict(sorted(final_rewards.items()))
    return final_rewards

@pytest.fixture(scope="session")
def merkle_tree(reward_amounts):
    hash_list = []
    i = 0
    for reward_address, reward_amount in reward_amounts.items():
        hash_list.append(web3.solidityKeccak(['address', 'uint256'], [web3.toChecksumAddress(reward_address), reward_amount]))
    merkleTree = MerkleTree()
    merkleTree.add_leaf(hash_list)
    merkleTree.make_tree()
    return merkleTree

