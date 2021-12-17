#!/usr/bin/python3

from conftest import *
from brownie.network.state import Chain
import random

sent_list = []

def test_claim_test(ERC20Contract, AirdropContract, merkle_tree, reward_amounts):
    addresses = []
    amounts = []
    for reward_address, reward_amount in reward_amounts.items():
        addresses.append(reward_address)
        amounts.append(reward_amount)
    print(merkle_tree.get_merkle_root().hex())
    for i in range(50):
        leaf = random.randint(0, 22170)
        receiver = addresses[leaf]
        amount = amounts[leaf]
        proof = merkle_tree.get_proof(leaf)
        while len(proof) < 15:
            proof.append(0)
        AirdropContract.claim(receiver, amount, proof, {"from": accounts[4]})
        sent_list.append(leaf)
        assert ERC20Contract.balanceOf(receiver) == amount

def test_already_received_test(ERC20Contract, AirdropContract, merkle_tree, reward_amounts):
    addresses = []
    amounts = []
    for reward_address, reward_amount in reward_amounts.items():
        addresses.append(reward_address)
        amounts.append(reward_amount)
    for i in range(50):
        leaf = random.randint(0, 22170)
        if leaf in sent_list:
            continue
        receiver = addresses[leaf]
        amount = amounts[leaf]
        proof = merkle_tree.get_proof(leaf)
        while len(proof) < 15:
            proof.append(0)
        AirdropContract.claim(receiver, amount, proof, {"from": accounts[4]})
        sent_list.append(leaf)
        with brownie.reverts("Already received"):
            AirdropContract.claim(receiver, amount, proof, {"from": accounts[4]})    
        assert ERC20Contract.balanceOf(receiver) == amount

def test_invalid_proof_test(ERC20Contract, AirdropContract, merkle_tree, reward_amounts):
    addresses = []
    amounts = []
    for reward_address, reward_amount in reward_amounts.items():
        addresses.append(reward_address)
        amounts.append(reward_amount)
    for i in range(50):
        leaf = random.randint(0, 22170)
        receiver = addresses[leaf]
        amount = amounts[leaf]
        proof = merkle_tree.get_proof(leaf)
        if leaf in sent_list:
            continue
        while len(proof) < 15:
            proof.append(0)
        with brownie.reverts("Invalid proof"):
            AirdropContract.claim(receiver, amount + 1, proof, {"from": accounts[4]})
        AirdropContract.claim(receiver, amount, proof, {"from": accounts[4]})
        sent_list.append(leaf)
        assert ERC20Contract.balanceOf(receiver) == amount

def test_return_token_test(ERC20Contract, AirdropContract, merkle_tree, reward_amounts):
    init_balance = ERC20Contract.balanceOf(accounts[3])
    withdraw_balance = ERC20Contract.balanceOf(AirdropContract)
    with brownie.reverts("Not finished"):
        AirdropContract.return_token()
    chain = Chain()
    chain.sleep(DURATION)
    AirdropContract.return_token()
    assert ERC20Contract.balanceOf(accounts[3]) == init_balance + withdraw_balance
