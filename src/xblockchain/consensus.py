import asyncio
import logging
from typing import List, Optional, Set
from urllib.parse import urlparse

import httpx

from xblockchain.exceptions import XBlockChainServerException
from xblockchain.models import Block
from xblockchain.pow import valid_proof

logger = logging.getLogger(__name__)


class Consensus:
    def __init__(self):
        self.nodes: Set[str] = set()

    def register_node(self, address: str) -> None:
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        else:
            raise XBlockChainServerException(status_code=400, detail=f"{address} is not a valid URL")

    @staticmethod
    def valid_chain(chain: List[Block]) -> bool:
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            logger.info(f'{last_block}')
            logger.info(f'{block}')
            logger.info("\n-----------\n")
            # Check that the hash of the block is correct
            if block.previous_hash != last_block.to_hash():
                return False

            # Check that the Proof of Work is correct
            if not valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1

        return True

    async def resolve_conflicts(self, current_chain: List[Block]) -> Optional[List[Block]]:
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: if our chain was replaced, returns new chain; else returns None
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(current_chain)

        async with httpx.AsyncClient() as client:
            # Grab and verify the chains from all the nodes in our network
            tasks = [client.get(f'http://{node}/chain') for node in neighbours]
            responses = await asyncio.gather(*tasks)

            for response in responses:
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = [Block(**block) for block in response.json()['chain']]

                    # Check if the length is longer and the chain is valid
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        return new_chain
