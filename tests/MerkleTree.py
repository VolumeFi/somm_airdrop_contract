from brownie import web3

class MerkleTree:
    def __init__(self):
        self.reset_tree()
    
    def reset_tree(self):
        self.leaves = list()
        self.levels = None
        self.is_ready = False
    
    def add_leaf(self, values):
        self.is_ready = False
        if not isinstance(values, tuple) and not isinstance(values, list):
            values = [values]
        for v in values:
            self.leaves.append(v)
    
    def get_leaf(self, index):
        return self.leaves[index]
    
    def get_leaf_count(self):
        return len(self.leaves)
    
    def get_tree_ready_state(self):
        return self.is_ready
    
    def _calculate_next_level(self):
        solo_leave = None
        N = len(self.levels[0])
        if N % 2 == 1:
            solo_leave = self.levels[0][-1]
            N -= 1
        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            if l < r:
                new_level.append(web3.keccak(l + r))
            else:
                new_level.append(web3.keccak(r + l))
        if solo_leave is not None:
            new_level.append(solo_leave)
        self.levels = [new_level, ] + self.levels

    def make_tree(self):
        self.is_ready = False
        if self.get_leaf_count() > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.is_ready = True

    def get_merkle_root(self):
        if self.is_ready:
            if self.levels is not None:
                return self.levels[0][0]
            else:
                return None
        else:
            return None

    def get_proof(self, index):
        if self.levels is None:
            return None
        elif not self.is_ready or index > len(self.leaves) - 1 or index < 0:
            return None
        else:
            proof = []
            for x in range(len(self.levels) - 1, 0, -1):
                level_len = len(self.levels[x])
                if (index == level_len - 1) and (level_len % 2 == 1):
                    index = int(index / 2.)
                    # proof.append(0)
                    continue
                is_right_node = index % 2
                sibling_index = index - 1 if is_right_node else index + 1
                sibling_value = self.levels[x][sibling_index]
                proof.append(sibling_value)
                index = int(index / 2.)
            return proof

    def validate_proof(self, proof, target_hash, merkle_root):
        merkle_root = merkle_root
        target_hash = target_hash
        if len(proof) == 0:
            return target_hash == merkle_root
        else:
            proof_hash = target_hash
            for p in proof:
                sibling = p
                proof_hash = web3.keccak(sibling + proof_hash if sibling < proof_hash else proof_hash + sibling)
            return proof_hash == merkle_root