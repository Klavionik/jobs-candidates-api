from fastapi import FastAPI
from app.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    @app.get("/healthz")
    async def healthz() -> str:
        return "OK"

    return app
