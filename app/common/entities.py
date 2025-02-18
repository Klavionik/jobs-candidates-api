from pydantic import BaseModel


class Job(BaseModel):
    id: int
    max_salary: int
    top_skills: list[str]
    other_skills: list[str]
    seniorities: list[str]


class Candidate(BaseModel):
    id: int
    salary_expectation: int
    top_skills: list[str]
    other_skills: list[str]
    seniority: str


class Hit(BaseModel):
    entity_id: int
    relevance_score: float
