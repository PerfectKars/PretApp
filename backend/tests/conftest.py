import os
from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, make_url, text
from sqlalchemy.orm import Session

from app.db import DATABASE_URL, get_session
from app.horloge import maintenant
from app.main import app

# Base dédiée aux tests : la base de développement n'est jamais touchée.
TEST_DATABASE_URL = make_url(
    os.environ.get("TEST_DATABASE_URL")
    or make_url(DATABASE_URL).set(database="pretapp_test")
)


def _creer_base_si_absente() -> None:
    serveur = create_engine(
        TEST_DATABASE_URL.set(database="postgres"), isolation_level="AUTOCOMMIT"
    )
    with serveur.connect() as connexion:
        existe = connexion.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :nom"),
            {"nom": TEST_DATABASE_URL.database},
        )
        if not existe:
            connexion.execute(text(f'CREATE DATABASE "{TEST_DATABASE_URL.database}"'))
    serveur.dispose()


def alembic_config() -> Config:
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url", TEST_DATABASE_URL.render_as_string(hide_password=False)
    )
    return config


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    """Base vide, puis toutes les migrations : vérifie aussi `upgrade` et
    `downgrade`."""
    _creer_base_si_absente()
    config = alembic_config()
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    moteur = create_engine(TEST_DATABASE_URL)
    yield moteur
    moteur.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Chaque test tourne dans une transaction annulée à la fin."""
    with engine.connect() as connexion:
        transaction = connexion.begin()
        with Session(
            bind=connexion, join_transaction_mode="create_savepoint"
        ) as session:
            yield session
        transaction.rollback()


# Horloge contrôlée : les tests ne dépendent jamais de l'heure réelle.
HEURE_SERVEUR = datetime(2026, 11, 1, 12, 0, tzinfo=UTC)


@pytest.fixture
def heure_serveur() -> datetime:
    return HEURE_SERVEUR


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[maintenant] = lambda: HEURE_SERVEUR
    yield TestClient(app)
    app.dependency_overrides.clear()
