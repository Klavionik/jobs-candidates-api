from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from app.es_lib.exceptions import EntityNotFoundError
from typing import Generic, TypeVar, Any, Optional, cast
from pydantic import BaseModel

Entity = TypeVar("Entity")


class Hit(BaseModel, Generic[Entity]):
    entity: Entity
    relevance_score: float


class ElasticsearchClient(Generic[Entity]):
    """
    Class containing methods for retrieving jobs or candidates from the
    respective Elasticsearch index by ID as well as sending queries.
    """

    def __init__(self, url: str, index: str) -> None:
        self._client = AsyncElasticsearch(url)
        self.index = index

    async def get_entity(
        self,
        *,
        id: int,
    ) -> Entity:
        """
        Returns the document corresponding to the given document ID as dictionary.

        Args:
            id (int): ID of the document to return.

        Returns:
            Entity: Entity object corresponding to the given ID.

        Raises:
            EntityNotFoundError: If entity with the given ID was not found in the index.
        """

        try:
            document = await self._client.get_source(
                index=self.index, id=str(id), source=True
            )
        except NotFoundError as error:
            msg = f"Entity {self.index} with ID {id} was not found."
            raise EntityNotFoundError(msg) from error

        # TODO: An adapter function.
        entity = cast(Entity, document)
        return entity

    async def search(
        self, query: dict[str, Any], return_source: bool = False
    ) -> list[Hit[Entity]]:
        """
        Executes a query on the index.
        """
        result = await self._client.search(
            body=query, index=self.index, source=return_source
        )

        # TODO: An adapter function.
        return cast(list[Hit[Entity]], result)

    async def search_with_bool_queries(
        self,
        *,
        should_queries: Optional[list[dict[str, Any]]] = None,
        must_queries: Optional[list[dict[str, Any]]] = None,
        return_source: bool = False,
    ) -> list[Hit[Entity]]:
        """
        Builds a boolean query comprising the provided should and must sub queries.

        Args:
            should_queries: the sub-queries that are to be concatenated by the OR operator
            must_queries: the sub-queries that are to be concatenated by the AND operator
            return_source: whether to return the _source field of the document.

        Returns:
            The matching documents.
        """
        if not (should_queries or must_queries):
            raise ValueError("Either should_queries or must_queries must be set.")

        query = {
            "query": {
                "bool": {"must": must_queries or [], "should": should_queries or []}
            }
        }
        result = await self.search(query=query, return_source=return_source)
        return result
