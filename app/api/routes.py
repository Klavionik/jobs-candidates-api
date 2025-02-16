from fastapi import APIRouter, Depends
from app.common.entities import Job, Candidate
from typing import Annotated
from app.api.di import (
    get_jobs_repository,
    get_candidates_repository,
)
from app.repositories import JobsRepository, CandidatesRepository

router = APIRouter(prefix="/api/v1")


@router.get("/candidates/{candidate_id}")
async def get_candidate(
    candidate_id: int,
    repository: Annotated[CandidatesRepository, Depends(get_candidates_repository)],
) -> Candidate:
    return await repository.get_by_id(candidate_id)


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: int, repository: Annotated[JobsRepository, Depends(get_jobs_repository)]
) -> Job:
    return await repository.get_by_id(job_id)
