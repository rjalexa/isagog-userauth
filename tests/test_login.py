import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from isagog_userauth.main import app
from isagog_userauth.models import Base, User
from isagog_userauth.utils import get_password_hash
from isagog_userauth.db_session import get_db

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)

    # Create a test user
    db = TestingSessionLocal()
    test_user = User(
        email="testuser@example.com",
        username="testuser",
        password=get_password_hash("testpassword"),
        role="basic",
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

    yield client

    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)


def test_login(client):
    response = client.post(
        "/user/login", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    # Optionally, add more checks to verify the tokens
    # For example, you can decode and verify the JWT tokens here
    import jwt
    from isagog_userauth.config import JWT_SECRET

    try:
        access_token_payload = jwt.decode(
            data["access_token"], JWT_SECRET, algorithms=["HS256"]
        )
        refresh_token_payload = jwt.decode(
            data["refresh_token"], JWT_SECRET, algorithms=["HS256"]
        )
        assert "sub" in access_token_payload
        assert "sub" in refresh_token_payload
    except jwt.PyJWTError as e:
        pytest.fail(f"JWT token verification failed: {e}")
