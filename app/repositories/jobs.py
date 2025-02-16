import abc
from app.common.entities import Job
from app.es_lib import ElasticsearchClient


class JobsRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, candidate_id: int) -> Job:
        pass


class ESJobsRepository(JobsRepository):
    def __init__(self, es_client: ElasticsearchClient):
        self._es_client = es_client

    async def get_by_id(self, job_id: int) -> Job:
        document = await self._es_client.get_entity(id=job_id)
        return Job(id=job_id, **document)
