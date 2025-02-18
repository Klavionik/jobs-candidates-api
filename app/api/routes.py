from fastapi import APIRouter, Depends
from app.common.entities import Job, Candidate, Hit
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


@router.get("/candidates/{candidate_id}/jobs")
async def search_jobs_by_candidate(
    candidate_id: int,
    candidates_repository: Annotated[
        CandidatesRepository, Depends(get_candidates_repository)
    ],
    jobs_repository: Annotated[JobsRepository, Depends(get_jobs_repository)],
    salary_match: bool = False,
    top_skills_match: bool = False,
    seniority_match: bool = False,
) -> list[Hit]:
    candidate = await candidates_repository.get_by_id(candidate_id)
    jobs = await jobs_repository.search_by_candidate(
        candidate, salary_match, top_skills_match, seniority_match
    )
    return jobs


@router.get("/jobs/{job_id}/candidates")
async def search_candidates_by_job(
    job_id: int,
    jobs_repository: Annotated[JobsRepository, Depends(get_jobs_repository)],
    candidates_repository: Annotated[
        CandidatesRepository, Depends(get_candidates_repository)
    ],
    salary_match: bool = False,
    top_skills_match: bool = False,
    seniority_match: bool = False,
) -> list[Hit]:
    job = await jobs_repository.get_by_id(job_id)
    candidates = await candidates_repository.search_by_job(
        job, salary_match, top_skills_match, seniority_match
    )
    return candidates
