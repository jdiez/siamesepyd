"""
To Do:
Unify protocol to get Short UUID from Long UUID and String.
Add ARK and PURL
Use blake3 for hashing.
Add hashlib for md5 hashing or whatever.
Add prefix or suffix to siamese right, so hashing siamese function is known.

Make temmplate purl:
{base_url}{resource_type}{project}{id}
ex: https://purl.astrazeneca.com/api/v1/sample/ENABLE/LUNG01234-XYZJAV
ex: https://purl.astrazeneca.com/api/v1/NCIT_C70699/ENABLE/LUNG01234-XYZJAV
proposal_id: LUN0234 [specified format]
            --> LUN0234-ALHMRW [siamese]
            --> NCIT_C70699/ENABLE/LUN0234-ALHMRW [locally namespaced siamese]
            --> 344756b91e226a2d0b781abb3e22a9d9 [uuid]
            --> [https://purl.astrazeneca.com/api/v1/][NS]/344756b91e226a2d0b781abb3e22a9d9
"""

__author__ = "Javier Díez Pérez"
__mail__ = "jdiezperezj@gmail.com"
__copyright__ = "Copyright 2021, AstraZeneca"
__license__ = "Apache License 2.0"


from collections import namedtuple
from enum import Enum
from typing import Callable
from uuid import UUID

from loguru import logger
from pydantic import BaseModel, HttpUrl

from siamesepyd.hashing import hashlib_uuid
from siamesepyd.shortids import ShortFromUUID


class Uri(Enum):
    """AI is creating summary for Uri

    Args:
        Enum ([type]): [description]
    """

    CURIE = "curie"
    URI = "uri"
    SIAMESE = "siamese"
    ALL = "all"


class MyUuidMetadataBaseModel(BaseModel):
    """AI is creating summary for MyBaseModel

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """

    salt: str | None = "uno"
    other: str | None = "dos"
    uri: HttpUrl | None = "http://example.org:8000/pid/"
    curie: str | None = "example"


class SiameseUUID:
    """AI is creating summary for SiameseUUIDs

    Args:
        uuid_function (Callable, optional): [description]. Defaults to partial(uuid5, NAMESPACE_OID).
        siamese_length (int, optional): [description]. Defaults to 6."""

    SiameseTuple = namedtuple("SiameseTuple", ["uuid", "siamese_key", "curie", "url"])

    def __init__(
        self,
        uuid_function: Callable = hashlib_uuid,  # partial(uuid5, NAMESPACE_OID),
        siamese_length: int = 6,
        key_seed: str = "",
        separator: str = "-",
        siamese_function: Callable = ShortFromUUID(),
        # Callable = lambda x, y: "".join([i.upper() for i in x if i.isalpha()][:y]),
    ) -> None:
        """AI is creating summary for __init__

        Args:
            uuid_function (Callable, optional): [description]. Defaults to partial(uuid5, NAMESPACE_OID).
            siamese_length (int, optional): [description]. Defaults to 5.
            key_seed (str, optional): [description]. Defaults to ''.
            siamese_function (Callable, optional): It takes uuid string and siamese key length and return a substring.
        """
        self.uuid = uuid_function  # implement return one type to avoid overhead and errors.
        self.siamese_length = siamese_length
        self.key_seed = key_seed
        self.separator = separator
        self.siamese_function = siamese_function

    def _get_key(self, data: str) -> UUID:
        """AI is creating summary for get_key

        Args:
            data (str): [description]

        Returns:
            UUID: [description]
        """
        try:
            result = self.uuid(self.key_seed + data)
        except TypeError as e:
            logger.error(f"Data should be a string. {e!s}")
        else:
            return result

    def validate_keys(self, left_side: str, right_side: str) -> bool:
        """Validata siamese keys.

        Args:
            left_side (str): Left hand side of the siamese key.
            right_side (str): Right hand side of the siamese key.

        Returns:
            bool: Keys validation or fail as boolean.
        """
        siamese_key = self._siamese(self._get_key(left_side))
        if siamese_key == right_side:
            res = True
        else:
            res = False
            logger.error(f"Left side: {left_side}, Right side: {right_side}")
        return res

    def _siamese(self, data: str | UUID) -> str:
        """AI is creating summary for _siamese

        Args:
            data (str): [description]

        Returns:
            str: [description]
        """
        match data:
            case str():
                result = self.siamese_function(data)
            case UUID():
                result = self.siamese_function(data.hex)
            case _:
                raise TypeError(f"Unknown data type: {type(data)}")  # noqa: TRY003
        return result

    def __call__(self, metadata: MyUuidMetadataBaseModel, uri: Uri | None = None) -> str | SiameseTuple:
        """Implements callable object.
        This should be refactored, so key serialization is under serialization function (inside or outside the model).

        Raises:
            TypeError: [description]

        Returns:
            [type]: [description]
        """
        try:
            data = str(self._get_key(metadata.salt))
        except TypeError:
            logger.error("Metadata salt should be a string.")
        else:
            match uri:
                case Uri.URI:
                    url = f"{metadata.uri}{data}"
                    res = url
                case Uri.CURIE:
                    curie = f"{metadata.curie}:{data}"
                    res = curie
                case Uri.SIAMESE:
                    g_key = self._siamese(data)
                    siamese_key = f"{metadata.salt}{self.separator}{g_key}"
                    res = siamese_key
                case Uri.ALL:
                    g_key = self._siamese(data)
                    siamese_key = f"{metadata.salt}{self.separator}{g_key}"
                    curie = f"{metadata.curie}:{data}"
                    url = f"{metadata.uri}{data}"
                    res = self.SiameseTuple(data, siamese_key, curie, url)
                case None:
                    res = data
                case _:
                    raise TypeError(f"Unknown uri: {uri}")  # noqa: TRY003
        return res


if __name__ == "__main__":
    Siamese = SiameseUUID(key_seed="ENABL")  # This could be replaced with project uuid.
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342")))
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342"), uri=Uri.CURIE))
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342"), uri=Uri.URI))
    print("Siamese key: ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342"), uri=Uri.SIAMESE))
    print("Proper UUID (uuid5): ", Siamese(MyUuidMetadataBaseModel(salt="LUNG342"), uri=Uri.ALL))
    print("Validated 'LUNG342', 'ABGZMV': ", Siamese.validate_keys("LUNG342", "ABGZMV"))
    print("Validated 'LUNG342', 'ABGZMY': ", Siamese.validate_keys("LUNG342", "ABGZMY"))
    print("Validated 'LUNG341', 'ABGZMV': ", Siamese.validate_keys("LUNG341", "ABGZMV"))
    print("\nExperected output:")
    print(
        """
        Proper UUID (uuid5):  05dff1df16ccf596b3d0950f5e90770b
        Proper UUID (uuid5):  example:05dff1df16ccf596b3d0950f5e90770b
        Proper UUID (uuid5):  http://example.org:8000/pid/05dff1df16ccf596b3d0950f5e90770b
        Siamese key:  LUNG342-ABGZMV
        Proper UUID (uuid5):  SiameseTuple(uuid='05dff1df16ccf596b3d0950f5e90770b',
                                            siamese_key='LUNG342-ABGZMV',
                                            curie='example:05dff1df16ccf596b3d0950f5e90770b',
                                            url='http://example.org:8000/pid/05dff1df16ccf596b3d0950f5e90770b')
        Validated 'LUNG342', 'ABGZMV':  True
        2023-12-21 12:26:38.270 | ERROR    | __main__:validate_keys:74 - Left side: LUNG342, Right side: ABGZMY
        Validated 'LUNG342', 'ABGZMY':  False
        2023-12-21 12:26:38.270 | ERROR    | __main__:validate_keys:74 - Left side: LUNG341, Right side: ABGZMV
        Validated 'LUNG341', 'ABGZMV':  False"""
    )
