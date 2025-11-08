from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .core.config import settings
from .core.logging import configure_logging


def create_app() -> FastAPI:
    """
    Build the FastAPI application instance.

    Returns
    -------
    FastAPI
        Configured application with routes, middleware, and metadata registered.
    """
    configure_logging()

    app = FastAPI(
        title="CareFlow AI API",
        version=settings.version,
        description=(
            "CareFlow AI orchestrates intelligent scheduling, reminders, and waitlist automations "
            "to reduce no-shows and improve healthcare access."
        ),
        contact={"name": "CareFlow AI Team", "email": "support@careflow.ai"},
    )

    # CORS setup for mobile and web clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/healthz", tags=["health"])
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
