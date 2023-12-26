"""Resource dataclasses.
"""

from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ResourceClass(BaseModel):
    """AI is creating summary for Resource

    Args:
        BaseModel ([type]): [description]
    """

    name: str
    _id: UUID
    uri: HttpUrl
    model_metadata: BaseModel


class ResourceInstance(BaseModel):
    """AI is creating summary for ResourceInstance

    Args:
        BaseModel ([type]): [description]
    """

    value: str
    resource_metadata: ResourceClass
    uri: HttpUrl | None = None
    uuid: UUID | None = None
    short_uuid: str | None = None
    siamese_id: str | None = None


class Project(BaseModel):
    """AI is creating summary for Project

    Args:
        BaseModel ([type]): [description]
    """

    project_id: UUID
    project_name: str  # regex
    project_description: str
    project_url: HttpUrl
    project_uri: HttpUrl


class Sample(BaseModel):
    """AI is creating summary for Sample

    Args:
        Enum ([type]): [description]
    """

    project_id: UUID
    biospecimen_uri: UUID  # linked resource
    purcharse_order_id: UUID
    sample_id: UUID
    sample_uri: HttpUrl
    sample_name: str  # regex
    original_id: str | None = None
    source_id: str | None = None
