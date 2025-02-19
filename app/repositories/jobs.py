import abc
from typing import Any

from app.common.entities import Job, Candidate, Hit
from app.es_lib import ElasticsearchClient, EntityNotFoundError


class JobsRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, job_id: int) -> Job | None:
        pass

    @abc.abstractmethod
    async def search_by_candidate(
        self,
        candidate: Candidate,
        salary_match: bool,
        top_skill_match: bool,
        seniority_match: bool,
    ) -> list[Hit]:
        pass


class ESJobsRepository(JobsRepository):
    def __init__(self, es_client: ElasticsearchClient):
        self._es_client = es_client

    async def get_by_id(self, job_id: int) -> Job | None:
        try:
            document = await self._es_client.get_entity(id=job_id)
        except EntityNotFoundError:
            return None

        return Job(id=job_id, **document)

    async def search_by_candidate(
        self,
        candidate: Candidate,
        salary_match: bool,
        top_skills_match: bool,
        seniority_match: bool,
    ) -> list[Hit]:
        query: list[dict[str, Any]] = []

        if salary_match:
            query.append(
                {"range": {"max_salary": {"gte": candidate.salary_expectation}}}
            )

        if top_skills_match:
            query.append(
                {
                    "terms_set": {
                        "top_skills": {
                            "terms": candidate.top_skills,
                            "minimum_should_match": min(len(candidate.top_skills), 2),
                        }
                    }
                }
            )

        if seniority_match:
            query.append({"term": {"seniority": {"value": candidate.seniority}}})

        docs = await self._es_client.search_with_bool_queries(must_queries=query)
        return [
            Hit(entity_id=hit["_id"], relevance_score=hit["_score"])
            for hit in docs["hits"]["hits"]
        ]
