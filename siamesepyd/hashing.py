"""Hashing functions module.
"""

import hashlib
from uuid import UUID


def hashlib_uuid(
    data: bytes | str,
    algorithm: str | None = "sha256",
    salt: bytes | None = b"",
    iterations: int | None = 10**6,
    dklen: int | None = 16,
) -> UUID:
    """AI is creating summary for hahlib_implementation

    Args:
        data (bin, str): [description]
        algorithm (bin, optional): [description]. Defaults to b'sha256'.
        salt (bin, optional): [description]. Defaults to b''.
        iterations (int, optional): [description]. Defaults to 10**6.
        dklen (int, optional): [description]. Defaults to 16.

    Returns:
        uuid.UUID: [description]
    """
    match data:
        case bytes():
            pass
        case str():
            data = data.encode()
        case _:
            raise TypeError(f"Data should be a string, not: {data}, {type(data)}.")  # noqa: TRY003
    return UUID(bytes=hashlib.pbkdf2_hmac(algorithm, data, salt, iterations, dklen))
