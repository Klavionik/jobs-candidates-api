# Candidates/Jobs API
Implementation of a simple Candidates/Jobs API for Instaffo. See the task description 
below.

## How to run
1. Clone the repository and `cd` into the project folder.
2. Run `$ docker compose up --wait` to start services and populate the database with mock 
   data.
3. As soon as all services are up and healthy, visit `http://localhost:8005/docs` in your 
   browser to see the OpenAPI docs and try out the API. 
4. You can use `$ docker compose run --rm api pytest -v` to run the test suite. 

See `covreport.txt` for the test coverage report. 


## The solution
To put it shortly, in the REST world we are expected to expose our resources via API 
endpoints for clients to perform HTTP requests on them. What you call a resource is up to 
you and depends on the scope of the problem, but in our case I believe that Jobs and 
Candidates are resources.

So here we have 4 endpoints: two for the Job resource and two for the Candidate resource.
One of each pair simply responds with an entity object and another allows for a filtered
search of a corresponding subresource (where "jobs" is a subresource of a candidate 
and "candidates" is a subresource of a job). Scoping information (like the ID of an 
entity to fetch or filters) is received via path and query parameters, contributing 
to the addressability of the API.

Code-wise, everything is pretty simple. Route handlers should not be responsible for 
anything, except for all things HTTP, like validating the request and sending the 
response. There is no business logic in this project, I would say, only some data access 
logic, which is encapsulated in repositories. So the route handlers in `app.api.routes` 
simply validate the incoming parameters, pass them down to repositories, and respond 
to clients with some data that has been retrieved via repositories. The repositories in 
`app.repositories` handle all the gritty stuff, issuing correct queries to the database 
and returning entities from `app.common.entities`, basically serving as a container of 
entities of a given type. 

I've introduced some small changes to the provided ElasticSearch boilerplate client and 
made it async. I also prefer to strictly typehint my code these days. It makes the 
development a bit slower and sometimes tricky, but allows for a much greater control 
of the codebase, saving me from a ton of bugs (especially during a big refactoring). There 
was no such requirement, but I made it mandatory to use at least one of the available 
filters (I guess it just makes sense).

What would I improve, if I had to develop this API further:
1. Obviously, there's a need for pagination for the search endpoints.
2. We probably should create one ES client at the startup and not on every request, so 
that we can make use of the HTTP connections pool.

# Intro

For your next step in the application process at Instaffo we'd like you to do the task given below to be able to further assess your skills and knowledge. 

**Submission Guidelines:**

✅ **Code Submission**: Please upload your solution to a **publicly accessible Git repository** and share the link with the person managing your application (e.g., via the chat on instaffo.com).

✅ **Video Explanation (Optional but Preferred)**: If possible, please record a **short video** explaining your overall solution (e.g., using [Loom](https://www.loom.com/screen-recorder)), and share the link with us.

Code quality (including project structure), dependencies and environment management, documentation (docstrings, comments, README file, etc.) are of utmost importance!

We wish you good luck (and also a lot of fun) with the task! 🍀

# Matching talents and jobs

Instaffo is a recruiting platform that makes money by bringing together hiring companies and talents. Companies offer job opportunities and need the right talents to fill their open job positions, talents on the other hand are looking for new job opportunities.

One core component of the Instaffo platform is the search functionality, which e.g. enables talents to only see relevant job opportunities.

# Task

You are provided with data and a docker-compose.yml file which initializes and populates __2 ES indices - for candidates and jobs__. 

🎯 Your goal is to create a way for the outside world to communicate with the ES indices.

📌 Implement 2 core functionalities:

1. Implement a functionality that, given an ID for either a job or a candidate, retrieves the corresponding document from the ES index.
2. Implement a functionality that, given a job ID or candidate ID, retrieves the corresponding candidates or jobs that match the user’s specified filters. The return value should contain the following fields - id of the matching documents as `id` and the relevance scores as `relevance_score`.
    - The filters, available to the user should be at least 2 of the following: `salary_match`, `top_skill_match` and `seniority_match`.
        - The `salary_match` filter should return jobs that have `gte` `max_salary` than the candidate's `salary_expectation` and should return candidates that have `lte` `salary_expectation` than a job's `max_salary`
        - The `top_skill_match` filter should return jobs/candidates that share at least min(<n_query_top_skills>, 2) of the top skills with the target document (job or candidate). Here, n_query_top_skills is the total number of top skills for the entity whose relevant matches we want to find. For example, if we are looking for relevant jobs for a given candidate, n_query_top_skills refers to the number of top skills that candidate has.
        - The `seniority_match` filter should return jobs/candidates where there is a match in the `seniorities` of a job and the `seniority` of a candidate.
    - The filters should be usable together, concatenated by the `OR` logical operator (`"should"` query in Elasticsearch).

    💡 The `_es_example.py` file provides examples on query building for all the required filters.  

Finally, update the existing docker-compose.yml file to include your new service, ensuring it can be accessed via HTTP requests. Additionally, provide a report on test coverage as part of your submission.
In your implementation you should abide to the principles of writing clean code and to the RestAPI design principles.

🪲 What we will assess:

- ❗ clean code
- ❗ well-defined api
- ❗ overall project structure
- 👶 some API tests **need** to be present but do **not** need to be detailed, devote only minimum effort, enough to showcase your understanding on how unit tests should be written.

## Good luck! 🚀
