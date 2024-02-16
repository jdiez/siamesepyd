"""FastAPI quick demo implementation.
Only for testing.
"""

from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from siamesepyd.core.siamese import MyUuidMetadataBaseModel, SiameseUUID


class Item(BaseModel):
    name: str
    description: str | None = None
    item_id: str
    metadata: str | None = None


# add favicon: https://dev.to/kludex/how-to-change-fastapis-swagger-favicon-4j6
app = FastAPI(
    title="Siamese Keys",
    description="Siamese Keys API at AZ.",  # could be markdown and render as html.
    summary="Amazing Siamese Keys API",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Amazing Siamese Keys API",
        "url": "http://x-force.example.com/contact/",
        "email": "jdiezperezj@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/get_siamese/{item_id}")
async def get_siamese(item_id: str) -> dict:
    """AI is creating summary for get_siamese

    Args:
        item_id (str): [description]

    Returns:
        dict: [description]
    """
    Siamese = SiameseUUID()  # This could be replaced with project uuid.
    return Siamese(MyUuidMetadataBaseModel(salt=item_id))._asdict()


@app.get("/validte_siamese/{item_id}")
async def validate_siamese(item_id: str, sep: str = "-") -> dict:
    """AI is creating summary for validate_siamese

    Args:
        item_id (str): [description]
        q (str, optional): [description]. Defaults to None.
        short (bool, optional): [description]. Defaults to False.

    Returns:
        dict: [description]
    """
    try:
        left, right = item_id.split(sep, maxsplit=1)
    except ValueError as e:
        logger.error(f"{e!s}")
    else:
        Siamese = SiameseUUID()  # This could be replaced with project uuid.
        data = Siamese(MyUuidMetadataBaseModel(salt=left))
        res = Siamese.validate_keys(left, right)
    return {
        "validated": res,
        "left": left,
        "right": right,
        "item_id": item_id,
        "siamese_key": data.siamese_key,
    }


@app.post("/create_uuid/")
async def create_uuid(item: Item) -> dict:
    """AI is creating summary for create_uuid

    Args:
        item (Item): [description]

    Returns:
        dict: [description]
    """
    return item.__dict__
