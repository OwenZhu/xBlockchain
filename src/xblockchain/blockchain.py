from time import time
from typing import List, Optional

from xblockchain.models import Transaction, Block


class Blockchain:
    def __init__(self):
        self.current_transactions: List[Transaction] = []
        self.chain: List[Block] = []

        # Create the genesis block
        _ = self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Block:
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <Block> New Block
        """

        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.chain[-1].to_hash()
        )

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Transaction) -> int:
        """
        Creates a new transaction to go into the next mined Block
        """
        self.current_transactions.append(transaction)

        return self.last_block.index + 1

    @property
    def last_block(self) -> Block:
        return self.chain[-1]
