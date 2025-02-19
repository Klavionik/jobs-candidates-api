from httpx import AsyncClient


async def test_healthz(test_client: AsyncClient) -> None:
    response = await test_client.get("/healthz")

    assert response.text == '"OK"'


async def test_get_job(test_client: AsyncClient) -> None:
    response = await test_client.get("/api/v1/jobs/1")
    job = response.json()

    assert response.status_code == 200
    assert job["id"] == 1


async def test_get_candidate(test_client: AsyncClient) -> None:
    response = await test_client.get("/api/v1/candidates/1")
    candidate = response.json()

    assert response.status_code == 200
    assert candidate["id"] == 1


async def test_get_job_404_if_not_found(test_client: AsyncClient) -> None:
    response = await test_client.get("/api/v1/jobs/9999")

    assert response.status_code == 404


async def test_get_candidate_404_if_not_found(test_client: AsyncClient) -> None:
    response = await test_client.get("/api/v1/candidates/9999")

    assert response.status_code == 404


async def test_search_jobs_by_candidate(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/api/v1/candidates/1/jobs?salary_match=true&top_skills_match=true&seniority_match=true"
    )
    jobs = response.json()

    assert response.status_code == 200
    assert jobs == [
        {"entity_id": 379, "relevance_score": 9.127895},
        {"entity_id": 401, "relevance_score": 9.127895},
        {"entity_id": 483, "relevance_score": 9.127895},
        {"entity_id": 485, "relevance_score": 9.127895},
    ]


async def test_search_candidates_by_job(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/api/v1/jobs/1/candidates?salary_match=true&top_skills_match=true&seniority_match=true"
    )
    candidates = response.json()

    assert response.status_code == 200
    assert candidates == [
        {"entity_id": 228, "relevance_score": 9.908987},
        {"entity_id": 248, "relevance_score": 9.908987},
    ]


async def test_search_jobs_by_candidate_400_if_no_filters(
    test_client: AsyncClient,
) -> None:
    response = await test_client.get("/api/v1/candidates/1/jobs")

    assert response.status_code == 400


async def test_search_candidates_by_job_400_if_no_filters(
    test_client: AsyncClient,
) -> None:
    response = await test_client.get("/api/v1/jobs/1/candidates")

    assert response.status_code == 400


async def test_search_jobs_by_candidate_404_if_not_found(
    test_client: AsyncClient,
) -> None:
    response = await test_client.get("/api/v1/candidates/9999/jobs?salary_match=true")

    assert response.status_code == 404


async def test_search_candidates_by_job_404_if_not_found(
    test_client: AsyncClient,
) -> None:
    response = await test_client.get("/api/v1/jobs/9999/candidates?salary_match=true")

    assert response.status_code == 404
