from typing import TypeVar, Generic

from pydantic import BaseModel

Entity = TypeVar("Entity")


class Hit(BaseModel, Generic[Entity]):
    entity: Entity
    relevance_score: float
