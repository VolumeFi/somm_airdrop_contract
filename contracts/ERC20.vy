# @version 0.3.1

event Transfer:
    _from: indexed(address)
    _to: indexed(address)
    _value: uint256

event Approval:
    _owner: indexed(address)
    _spender: indexed(address)
    _value: uint256

balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)
name: immutable(String[256])
symbol: immutable(String[32])

@external
def __init__(name_: String[256], symbol_: String[32]):
    name = name_
    symbol = symbol_
    self.balanceOf[msg.sender] = 5 * 10 ** 6 * 10 ** 18
    self.totalSupply = 5 * 10 ** 6 * 10 ** 18

@external
@view
def name() -> String[256]:
    return name

@external
@view
def symbol() -> String[32]:
    return symbol

@external
@pure
def decimals() -> uint256:
    return 18

@external
def transfer(recipient: address, amount: uint256) -> bool:
    assert recipient != ZERO_ADDRESS, "ERC20: transfer to the zero address"
    self.balanceOf[msg.sender] -= amount
    self.balanceOf[recipient] += amount
    log Transfer(msg.sender, recipient, amount)
    return True

@external
def transferFrom(sender: address, recipient: address, amount: uint256) -> bool:
    assert sender != ZERO_ADDRESS, "ERC20: transfer from the zero address"
    assert recipient != ZERO_ADDRESS, "ERC20: transfer to the zero address"
    self.balanceOf[sender] -= amount
    self.balanceOf[recipient] += amount
    self.allowance[sender][msg.sender] -= amount
    log Transfer(sender, recipient, amount)
    return True

@external
def approve(_spender : address, _value : uint256) -> bool:
    assert _value == 0 or self.allowance[msg.sender][_spender] == 0
    self.allowance[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True