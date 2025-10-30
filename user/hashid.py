from django.conf import settings
from hashids import Hashids

hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=settings.HASHIDS_MIN_LENGTH)

def encode_id(pk: int) -> str:
    """
    id to hashid
    """
    return hashids.encode(pk)

def decode_id(hashid: str) -> int | None:
    """
    hashid to id
    """
    decoded = hashids.decode(hashid)
    return decoded[0] if decoded else None
