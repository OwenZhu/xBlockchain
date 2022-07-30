import logging
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from xblockchain.blockchain import Blockchain
from xblockchain.consensus import Consensus
from xblockchain.models import Transaction, NodeList
from xblockchain.pow import proof_of_work

app = FastAPI()

# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate Consensus Module
con = Consensus()

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return node_identifier


@app.get("/mine")
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(Transaction(sender="0", recipient=node_identifier, amount=1))

    # Forge the new Block by adding it to the chain
    previous_hash = last_block.to_hash()
    block = blockchain.new_block(proof, previous_hash)

    return {
        'message': "New Block Forged",
        'block': block
    }


@app.post("/transactions")
def new_transaction(transaction: Transaction):
    """
    Create a new Transaction
    """
    index = blockchain.new_transaction(transaction)
    return {'message': f'Transaction will be added to Block {index}'}


@app.get("/chain")
def get_full_chain():
    return {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }


@app.post('/nodes/register')
def register_nodes(data: NodeList):
    for node in data.nodes:
        con.register_node(node)

    return {
        'message': 'New nodes have been added',
        'total_nodes': list(con.nodes),
    }


@app.get('/nodes/resolve')
async def resolve_conflicts():
    message = "Our chain is authoritative"

    new_chain = await con.resolve_conflicts(blockchain.chain)

    if new_chain:
        blockchain.chain = new_chain
        message = 'Our chain was replaced'

    return {
        'message': message,
        'chain': blockchain.chain
    }


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)
