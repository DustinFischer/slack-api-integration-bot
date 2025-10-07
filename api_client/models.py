from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ObjectCategory(Enum):
    SERVICE = 'Service'
    SYSTEM = 'System'
    PEOPLE = 'People'
    TAGS = 'Tags'
    ORGANISATIONS = 'Organisations'
    FUNCTIONAL_AREAS = 'Functional Areas'
    LAYERS = 'Layers'
    TECHNOLOGIES = 'Technologies'


class ImageKey(Enum):
    KUBERNETES = 'Kubernetes'
    SYSTEMDB = 'SystemDB'
    GITHUB = 'GitHub'
    JIRA = 'Jira'

class DataSourceType(Enum):
    PIPELINE = 'pipeline'
    USER = 'user'
    LOADER = 'loader'


class LayerName(Enum):
    CLIENT = 'Client'


class LifeCycleStage(Enum):
    PRIMARY = 'Primary'


class ObjectRole(Enum):
    SERVICE = 'Service'
    STORE = 'Store'


class ObjectStatus(Enum):
    PRODUCTION = 'Production'


class ObjectRelationship(BaseModel):
    calledBy: int
    calls: int


class DataSource(BaseModel):
    imageKey: Optional[ImageKey]
    name: str
    type: DataSourceType
    uiLink: Optional[str]


class TagCategory(Enum):
    TAGGED = 'Tagged'


class Tag(BaseModel):
    assignable: bool
    category: TagCategory
    editable: bool
    modelEntityName: str
    name: str
    owner: str
    public: bool


class Technology(BaseModel):
    imageLink: str
    name: str


class ObjectPreview(BaseModel):
    active: bool
    areaName: str
    category: ObjectCategory
    dataSources: List[DataSource]
    lastConfirmed: str  # TODO: datetime?
    lifeCycleStage: LifeCycleStage
    objectDescription: str
    objectName: str
    objectRole: ObjectRole
    owner: str
    qualityScore: int
    relationships: ObjectRelationship
    status: ObjectStatus
    tags: List[Tag]
    technologies: List[Technology]
    ttl: str
