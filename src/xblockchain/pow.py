import hashlib


def valid_proof(last_proof: int, proof: int) -> bool:
    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
    """

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"


def proof_of_work(last_proof: int) -> int:
    """
    Simple Proof of Work Algorithm:
     - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
     - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof
