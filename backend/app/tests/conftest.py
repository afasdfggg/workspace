import os
import pytest
from typing import Dict, Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a fresh database for each test.
    """
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up the database after each test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Generator) -> Generator:
    """
    Create a test client with a database session.
    """
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Reset the dependency override
    app.dependency_overrides = {}