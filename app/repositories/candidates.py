import abc
from app.common.entities import Candidate
from app.es_lib import ElasticsearchClient


class CandidatesRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, candidate_id: int) -> Candidate:
        pass


class ESCandidatesRepository(CandidatesRepository):
    def __init__(self, es_client: ElasticsearchClient):
        self._es_client = es_client

    async def get_by_id(self, candidate_id: int) -> Candidate:
        document = await self._es_client.get_entity(id=candidate_id)
        return Candidate(id=candidate_id, **document)
