from brownie import Airdrop, ERC20, accounts

def main():
    acct = accounts.load("myaccount")
    SOMM_ADDRESS = ERC20.deploy("Test ERC20", "T20", {"from": acct})
    DURATION = 60 * 60 * 24 * 30 * 6 # 6 months
    AIRDROP_ADDRESS = Airdrop.deploy(SOMM_ADDRESS, 0x23e8b2aab9ad8a3552bab04132fc4e41579d5b4a4cc6ca6836823e5be5b1e66a, acct, DURATION, {"from": acct})
    SOMM_ADDRESS.transfer(AIRDROP_ADDRESS, 5 * 10 ** 6 * 10 ** 18, {"from": acct})
