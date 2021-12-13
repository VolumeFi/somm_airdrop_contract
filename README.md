# Somm Airdrop Contract

## Testing and Development on testnet

### Dependencies

* [nodejs](https://nodejs.org/en/download/) - >=v8, tested with version v16.13.1
* [python3](https://www.python.org/downloads/release/python-368/) from version 3.6 to 3.9, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.17.2](https://github.com/eth-brownie/brownie/releases/tag/v1.17.2)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.2](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.2)



###  Deploy on testnet

```bash
brownie run scripts/deploy_tesnet.py --network rinkeby
```



###  Deploy on mainnet

Replace `SOMM` token address and `Gravity Bridge` Address in `scripts/deploy_mainnet.py`

```bash
brownie run scripts/deploy_mainnet.py --network mainnet
```
Transfer `SOMM` token to the airdrop address.



### Running the Tests

```bash
brownie test
```



### Contracts

- Airdrop - Main contract to airdrop using Merkle tree
- ERC20 - Test ERC20 contract



## External functions

| Function Name  | Parameters                                                 | Note | Description                                              |
| -------------- | ---------------------------------------------------------- | ---- | -------------------------------------------------------- |
| claim          | address receiver, uint256 amount, Bytes32[15] merkle_proof |      | claim function to airdrop. verify merkle proof with root |
| return_tokens  |                                                            |      | return all remaining tokens to `Gravity` after deadline  |
| somm_token     |                                                            | view | SOMM_TOKEN address                                       |
| received       | address receiver                                           | view | returns `true` if received once                          |
| deadline       |                                                            | view | airdrop deadline                                         |
| gravity_bridge |                                                            | view | Gravity Bridge address                                   |
| merkle_root    |                                                            | view | root of merkle tree                                      |
