from collections.abc import AsyncIterator

from app.es_lib.elastic_search_client import ElasticsearchClient
from typing import Annotated
from app.repositories import (
    ESJobsRepository,
    ESCandidatesRepository,
    JobsRepository,
    CandidatesRepository,
)
from app.common.config import Config
from fastapi import Depends


def get_config() -> Config:
    return Config()


async def get_jobs_repository(
    config: Annotated[Config, Depends(get_config)],
) -> AsyncIterator[JobsRepository]:
    es_client = ElasticsearchClient(config.es_url, index="jobs")

    try:
        yield ESJobsRepository(es_client)
    finally:
        await es_client.close()


async def get_candidates_repository(
    config: Annotated[Config, Depends(get_config)],
) -> AsyncIterator[CandidatesRepository]:
    es_client = ElasticsearchClient(config.es_url, index="candidates")

    try:
        yield ESCandidatesRepository(es_client)
    finally:
        await es_client.close()
