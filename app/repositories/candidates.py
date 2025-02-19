import abc
from typing import Any

from app.common.entities import Candidate, Hit, Job
from app.es_lib import ElasticsearchClient, EntityNotFoundError


class CandidatesRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, candidate_id: int) -> Candidate | None:
        pass

    @abc.abstractmethod
    async def search_by_job(
        self,
        job: Job,
        salary_match: bool,
        top_skills_match: bool,
        seniority_match: bool,
    ) -> list[Hit]:
        pass


class ESCandidatesRepository(CandidatesRepository):
    def __init__(self, es_client: ElasticsearchClient):
        self._es_client = es_client

    async def get_by_id(self, candidate_id: int) -> Candidate | None:
        try:
            document = await self._es_client.get_entity(id=candidate_id)
        except EntityNotFoundError:
            return None

        return Candidate(id=candidate_id, **document)

    async def search_by_job(
        self,
        job: Job,
        salary_match: bool,
        top_skills_match: bool,
        seniority_match: bool,
    ) -> list[Hit]:
        query: list[dict[str, Any]] = []

        if salary_match:
            query.append({"range": {"salary_expectation": {"lte": job.max_salary}}})

        if top_skills_match:
            query.append(
                {
                    "terms_set": {
                        "top_skills": {
                            "terms": job.top_skills,
                            "minimum_should_match": min(len(job.top_skills), 2),
                        }
                    }
                }
            )

        if seniority_match:
            query.append({"terms": {"seniority": job.seniorities}})

        docs = await self._es_client.search_with_bool_queries(must_queries=query)
        return [
            Hit(entity_id=hit["_id"], relevance_score=hit["_score"])
            for hit in docs["hits"]["hits"]
        ]
