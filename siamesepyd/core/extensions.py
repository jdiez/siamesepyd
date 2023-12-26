"""Extensions for the generation of UUIDs.
"""

from collections import namedtuple

from blake3 import blake3


class Blake3UUID:
    """AI is creating summary for"""

    shortBlakeUuid = namedtuple("ShortBlakeUUID", ["uuir", "shorted"])

    def __init__(self, context: str) -> None:
        """# Use the key derivation mode, which takes a context string. Context strings
            # should be hardcoded, globally unique, and application-specific.
            Source:https://github.com/oconnor663/blake3-py
        Args:
            context (str): [description]
        """
        self.context = context

    def _uuid(self, key_mat: str, key_context: bool = False) -> str:
        """AI is creating summary for _uuid

        Args:
            key_mat (str): [description]
            key_context (bool, optional): [description]. Defaults to False.

        Returns:
            str: [description]
        """

        _res = blake3(key_mat, derive_key_context=self.context).hex() if key_context else blake3(key_mat).hex()
        return _res

    def short_uid(self, key_mat: str, length: int = 6) -> namedtuple:
        """It return an alphabetical short uuid based on blake3 hash.

        Args:
            _uuid (str): [description]
            length (int, optional): [description]. Defaults to 6.

        Returns:
            namedtuple: [description]
        """
        _res = self._uuid(key_mat)
        _shorted = "".join([i.upper() for i in _res[::-1] if i.isalpha][:length])
        return self.shortBlakeUuid(uuid=_res, shorted=_shorted)
