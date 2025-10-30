import pytest
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.db_models import UserDB


@pytest.fixture
def mock_db():
    """Mock database session"""
    db = MagicMock()
    db.query.return_value = MagicMock()
    db.add.return_value = None
    db.commit.return_value = None
    db.refresh.return_value = None
    db.delete.return_value = None
    return db


@pytest.fixture
def client(mock_db):
    """Create test client with mocked database"""
    def override_get_db():
        yield mock_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "John Doe",
        "age": 30,
        "address": "123 Main Street"
    }


@pytest.fixture
def sample_user_db():
    """Sample user database object"""
    user = UserDB(
        id=1,
        name="John Doe",
        age=30,
        address="123 Main Street"
    )
    return user

