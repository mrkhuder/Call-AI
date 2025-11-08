from __future__ import annotations

from typing import Generator, List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.main import create_app
from app.db import session as db_session
from app.api.v1.endpoints.reminders import get_reminder_service as reminder_dependency
from app.integrations.messaging import ReminderDispatch
from app.services import ReminderService
from app import models  # noqa: F401  # ensure metadata is populated


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


@pytest.fixture()
def sent_reminders() -> List[ReminderDispatch]:
    return []


@pytest.fixture()
def client(engine, sent_reminders) -> Generator[TestClient, None, None]:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    db_session.engine = engine

    def get_session_override() -> Generator[Session, None, None]:
        session = Session(engine)
        try:
            yield session
        finally:
            session.close()

    class CapturingMessagingProvider:
        def __init__(self, store: List[ReminderDispatch]) -> None:
            self.store = store

        async def enqueue(self, payload: ReminderDispatch) -> str:
            self.store.append(payload)
            return payload.reminder_id

    def override_reminder_service() -> Generator[ReminderService, None, None]:
        session = Session(engine)
        provider = CapturingMessagingProvider(sent_reminders)
        service = ReminderService(session=session, messaging_provider=provider)
        try:
            yield service
        finally:
            session.close()

    test_app = create_app()
    test_app.router.on_startup.clear()
    test_app.router.on_shutdown.clear()

    test_app.dependency_overrides[db_session.get_session] = get_session_override
    test_app.dependency_overrides[reminder_dependency] = override_reminder_service

    with TestClient(test_app) as test_client:
        yield test_client

    test_app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)
