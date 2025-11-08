from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from alembic import command
from alembic.config import Config
from sqlmodel import Session, create_engine

from ..core.config import settings


def _build_engine():
    connect_args = {"check_same_thread": False} if settings.db_url.startswith("sqlite") else {}
    return create_engine(settings.db_url, echo=settings.db_echo, connect_args=connect_args)


engine = _build_engine()


def get_alembic_config() -> Config:
    base_path = Path(__file__).resolve().parents[2]
    alembic_ini_path = base_path / "alembic.ini"
    cfg = Config(str(alembic_ini_path))
    cfg.set_main_option("script_location", str(base_path / "alembic"))
    cfg.set_main_option("sqlalchemy.url", settings.db_url)
    return cfg


def init_db() -> None:
    cfg = get_alembic_config()
    command.upgrade(cfg, "head")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()