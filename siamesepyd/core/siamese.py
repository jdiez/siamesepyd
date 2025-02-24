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
from typing import Callable
from uuid import UUID

from loguru import logger
from pydantic import BaseModel, HttpUrl

from siamesepyd.core.hashing import hashlib_uuid
from siamesepyd.core.shortids import ShortFromUUID


class SiameseResult(BaseModel):
    """AI is creating summary for SiameseResult

    Args:
        BaseModel ([type]): [description]"""

    data: str
    siamese_key: str
    curie: str  # define curie as specific type (constr with specific regex).
    url: HttpUrl


class MyUuidMetadataBaseModel(BaseModel):
    """AI is creating summary for MyBaseModel

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """

    salt: str = "uno"
    uri: HttpUrl = "http://example.org:8000/pid/"
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
        return result if isinstance(result, UUID) else UUID(result)

    def validate_keys(self, left_side: str, right_side: str) -> bool:
        """Validata siamese keys.

        Args:
            left_side (str): Left hand side of the siamese key.
            right_side (str): Right hand side of the siamese key.

        Returns:
            bool: Keys validation or fail as boolean.
        """
        siamese_key = self._siamese(self._get_key(left_side))
        return siamese_key == right_side

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
        return str(result)

    def __call__(self, metadata: MyUuidMetadataBaseModel) -> SiameseTuple:
        """Generate a siamese key.

        Args:
            metadata (MyUuidMetadataBaseModel): object containing salt, other, uri.

        Raises:
            TypeError: [description]

        Returns:
            (SiameseTuple): [description]
        """
        try:
            data = str(self._get_key(metadata.salt))
            g_key = self._siamese(data)
        except TypeError:
            logger.error("Metadata salt should be a string. {e!s}")
        else:
            try:
                siamese_key = f"{metadata.salt}{self.separator}{g_key}"
                curie = f"{metadata.curie}:{data}"
                url = f"{metadata.uri}{data}"
            except AttributeError:
                logger.error("Attribute not found in metadata. {e!s}")
        return self.SiameseTuple(data, siamese_key, curie, url)
