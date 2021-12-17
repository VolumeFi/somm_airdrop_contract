# @version 0.3.1

TRANSFER_MID: constant(Bytes[4]) = method_id("transfer(address,uint256)")
MERKLE_TREE_DEPTH: constant(uint256) = 15

SOMM_TOKEN: immutable(address)
received: public(HashMap[address, bool])
DEADLINE: immutable(uint256)
GRAVITY_BRIDGE: immutable(address)
MERKLE_ROOT: immutable(bytes32)

interface IERC20:
    def balanceOf(owner: address) -> uint256: view

@external
def __init__(_somm_token: address, _merkle_root: bytes32, _gravity_bridge: address):
    SOMM_TOKEN = _somm_token
    DEADLINE = block.timestamp + 60 * 60 * 24 * 30 * 6 # 6 months
    GRAVITY_BRIDGE = _gravity_bridge
    MERKLE_ROOT = _merkle_root

@internal
def _safe_transfer(_token: address, _to: address, _value: uint256):
    _response: Bytes[32] = raw_call(
        _token,
        concat(
            TRANSFER_MID,
            convert(_to, bytes32),
            convert(_value, bytes32)
        ),
        max_outsize=32
    )  # dev: failed approve
    if len(_response) > 0:
        assert convert(_response, bool), "Transfer failed"  # dev: failed approve

@internal
@pure
def verify(proof:bytes32[MERKLE_TREE_DEPTH], root: bytes32, leaf: bytes32) -> bool:
    computed_hash: bytes32 = leaf
    for i in range(MERKLE_TREE_DEPTH):
        proof_element: bytes32 = proof[i]
        if convert(proof_element, uint256) != 0:
            if convert(computed_hash, uint256) <= convert(proof_element, uint256):
                computed_hash = keccak256(concat(computed_hash, proof_element))
            else:
                computed_hash = keccak256(concat(proof_element, computed_hash))
    return computed_hash == root

@external
@view
def somm_token() -> address:
    return SOMM_TOKEN

@external
@view
def gravity_bridge() -> address:
    return GRAVITY_BRIDGE

@external
@view
def merkle_root() -> bytes32:
    return MERKLE_ROOT

@external
@view
def deadline() -> uint256:
    return DEADLINE

@external
def claim(receiver: address, amount: uint256, merkle_proof: bytes32[MERKLE_TREE_DEPTH]):
    assert block.timestamp <= DEADLINE
    assert not self.received[receiver], "Already received"
    node: bytes32 = keccak256(concat(slice(convert(receiver, bytes32), 12, 20), convert(amount, bytes32)))
    assert self.verify(merkle_proof, MERKLE_ROOT, node), "Invalid proof"
    self._safe_transfer(SOMM_TOKEN, receiver, amount)
    self.received[receiver] = True

@external
def return_token():
    assert DEADLINE < block.timestamp, "Not finished"
    bal: uint256 = IERC20(SOMM_TOKEN).balanceOf(self)
    assert bal > 0, "Insufficient balance"
    self._safe_transfer(SOMM_TOKEN, GRAVITY_BRIDGE, bal)
