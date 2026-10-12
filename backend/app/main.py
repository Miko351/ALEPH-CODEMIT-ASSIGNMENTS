from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker

from app.api.auth import router
from app.core.config import Settings
from app.core.security import MemberSecurity
from app.db.base import Base
from app.db.session import build_engine


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    engine = build_engine(config.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(engine)
        yield
        engine.dispose()

    app = FastAPI(title="ALEPH 회원가입 API", version="1.0.0", lifespan=lifespan)
    app.state.session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app.state.security = MemberSecurity(config)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_methods=["POST", "GET"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError):
        # Never echo request inputs: validation errors may contain a password.
        errors = [
            {"loc": item["loc"], "type": item["type"], "msg": "입력값을 확인해 주세요."}
            for item in error.errors()
        ]
        return JSONResponse(status_code=422, content={"detail": errors})

    @app.get("/api/health", tags=["상태"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(router)
    return app
