from brownie import Airdrop, ERC20, accounts

def main():
    acct = accounts.load("deployer_account")
    SOMM_ADDRESS = "0x0000000000000000000000000000000000000000"
    GRAVITY_BRIDGE_ADDRESS = "0x0000000000000000000000000000000000000000"
    DURATION = 60 * 60 * 24 * 30 * 6 # 6 months
    Airdrop.deploy(SOMM_ADDRESS, 0x23e8b2aab9ad8a3552bab04132fc4e41579d5b4a4cc6ca6836823e5be5b1e66a, GRAVITY_BRIDGE_ADDRESS, DURATION, {"from": acct})

