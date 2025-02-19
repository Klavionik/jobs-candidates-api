from fastapi import APIRouter, Depends, HTTPException
from app.common.entities import Job, Candidate, Hit
from typing import Annotated
from app.api.di import (
    get_jobs_repository,
    get_candidates_repository,
)
from app.repositories import JobsRepository, CandidatesRepository

router = APIRouter(prefix="/api/v1")


@router.get("/candidates/{candidate_id}", summary="Get a Candidate by its ID.")
async def get_candidate(
    candidate_id: int,
    repository: Annotated[CandidatesRepository, Depends(get_candidates_repository)],
) -> Candidate:
    candidate = await repository.get_by_id(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=404, detail=f"Cannot find Candidate with ID {candidate_id}."
        )

    return candidate


@router.get("/jobs/{job_id}", summary="Get a Job by its ID.")
async def get_job(
    job_id: int, repository: Annotated[JobsRepository, Depends(get_jobs_repository)]
) -> Job:
    job = await repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404, detail=f"Cannot find Job with ID {job_id}."
        )

    return job


@router.get(
    "/candidates/{candidate_id}/jobs",
    summary="Search jobs for a Candidate with the given ID.",
)
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
    filter_provided = any((salary_match, top_skills_match, seniority_match))

    if not filter_provided:
        raise HTTPException(
            status_code=400,
            detail="You must provide at least one of these three filters: "
            "salary_match, top_skills_match, seniority_match.",
        )

    candidate = await candidates_repository.get_by_id(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=404, detail=f"Cannot find Candidate with ID {candidate_id}."
        )

    jobs = await jobs_repository.search_by_candidate(
        candidate, salary_match, top_skills_match, seniority_match
    )
    return jobs


@router.get(
    "/jobs/{job_id}/candidates",
    summary="Search candidates for a Job with the given ID.",
)
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
    filter_provided = any((salary_match, top_skills_match, seniority_match))

    if not filter_provided:
        raise HTTPException(
            status_code=400,
            detail="You must provide at least one of these three filters: "
            "salary_match, top_skills_match, seniority_match.",
        )

    job = await jobs_repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404, detail=f"Cannot find Job with ID {job_id}."
        )

    candidates = await candidates_repository.search_by_job(
        job, salary_match, top_skills_match, seniority_match
    )
    return candidates
