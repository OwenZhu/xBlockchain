import hashlib
import json
from typing import List

from pydantic import BaseModel, validator


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int

    @validator('amount')
    def name_must_contain_space(cls, v):
        if v < 1:
            raise ValueError("Amount must be larger or equal than 1")
        return v


class Block(BaseModel):
    index: int
    timestamp: float
    transactions: List[Transaction]
    proof: int
    previous_hash: str

    def to_hash(self) -> str:
        """
        Creates an SHA-256 hash of a Block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(self.dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class NodeList(BaseModel):
    nodes: List[str]
