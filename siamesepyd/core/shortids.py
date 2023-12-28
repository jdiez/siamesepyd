"""Short ids creation module
Could be cleaned up to be used in other modules.
As both modeles use .encode attribute and need to transform or clean input.
To be done
"""

import string
from typing import Callable
from uuid import UUID

import shortuuid
from loguru import logger
from sqids import Sqids


class ShortFromUUID:
    """Deterministic generation of Short UUID from Long UUID and String."""

    def __init__(self, alphabet: str = string.ascii_uppercase, length: int | None = 6) -> None:
        self.alphabet = self._clean_alphabet(alphabet)
        self.length = length
        # shortuuid.set_alphabet(self.alphabet)  # figure out how to set the alphabet cleanly.
        self.shrtuuid = shortuuid.ShortUUID(alphabet=self.alphabet)

    def _clean_alphabet(self, data: str) -> str:
        """Clean non-alphanumeric characters from string.
            Ideally only uppercase characters should be allowed, as default alphabet is ascii_uppercase.

        Args:
            data (str): [description]

        Returns:
            str: [description]
        """
        try:
            res = "".join({i for i in data if i.isalnum()})
        except TypeError as e:
            logger.error(f"Data should be a string. {e!s}")
        return res

    def __call__(self, data: str | UUID) -> str:
        """AI is creating summary for __call__

        Args:
            _uuid (str): [description]

        Raises:
            TypeError: [description]

        Returns:
            str: [description]
        """
        match data:
            case UUID():
                pass
            case str():
                try:
                    data = UUID(data)
                except ValueError as e:
                    logger.error(f"Invalid uuid: {data}. {e!s}")

            case _:
                raise TypeError(f"Unknown uuid: {data} format.")  # noqa: TRY003
        _short = str(self.shrtuuid.encode(data))
        data_length = len(str(_short))
        length = min(data_length, self.length) if self.length is not None else data_length
        return _short[:length]


class SeqIds:
    """Non deterministic generation of Short UUID from Long UUID and String."""

    def __init__(
        self,
        alphabet: str = string.ascii_uppercase,
        length: int | None = 6,
        str2int_func: Callable = lambda x: [ord(i.upper()) for i in x],
    ) -> None:
        """AI is creating summary for __init__

        Args:
            alphabet (str): [description]
        """
        self.alphabet = alphabet
        self.sqids = Sqids(alphabet=self._clean_alphabet(self.alphabet))
        self.length = length
        self.str2int_func = str2int_func

    def _clean_alphabet(self, data: str) -> str:
        """AI is creating summary for _alphabet

        Args:
            data (str): [description]

        Returns:
            str: [description]
        """
        try:
            _res = "".join({i for i in data if i.isalnum()})
        except TypeError as e:
            logger.error(f"Data should be a string. {e!s}")
        return _res

    def __call__(self, data: str) -> str:
        """AI is creating summary for __call__

        Args:
            data (str): [description]

        Returns:
            str: [description]
        """
        try:
            res = self.sqids.encode(self.str2int_func(data))
        except TypeError as e:
            logger.error(f"Data should be a string. {e!s}")
        else:
            length = min(len(res), self.length) if self.length is not None else len(res)
        return str(res[:length])
