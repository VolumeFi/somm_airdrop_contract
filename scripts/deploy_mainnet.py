from brownie import Airdrop, ERC20, accounts

def main():
    acct = accounts.load("deployer_account")
    SOMM_ADDRESS = "0xa670d7237398238DE01267472C6f13e5B8010FD1"
    GRAVITY_BRIDGE_ADDRESS = "0x69592e6f9d21989a043646fE8225da2600e5A0f7"
    DURATION = 60 * 60 * 24 * 30 * 3 # 3 months
    Airdrop.deploy(SOMM_ADDRESS, 0x96b4451e4392b6b1566a75b27ff13805f33f92c909c306840389711ad5069cf0, GRAVITY_BRIDGE_ADDRESS, DURATION, {"from": acct})

