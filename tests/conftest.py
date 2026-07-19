from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database import get_db
from app.main import app

settings = get_settings()

test_engine = create_engine(
    settings.test_database_url
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE visits, sites
                RESTART IDENTITY CASCADE
                """
            )
        )

    yield

    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE visits, sites
                RESTART IDENTITY CASCADE
                """
            )
        )
        

@pytest.fixture
def db_session() -> Generator[Session, None]:
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    