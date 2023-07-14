import hashlib


def generate_hash(value: str) -> str:
    '''
    Generate a SHA-256 hash and return it
    '''
    return hashlib.sha256(value.encode()).hexdigest()
