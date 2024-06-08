""" initialize the users database and initialize it with an admin user from the .env file """

import os

from dotenv import load_dotenv

from .base import Base
from .db_session import SessionLocal, engine
from .models import User
from .utils import get_password_hash

# Load environment variables
load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def init_db():
    """
    Initialize the database and create the initial admin user if it does not exist.

    This function performs the following actions:
    1. Creates all database tables defined by the SQLAlchemy models.
    2. Checks if an admin user exists in the database.
    3. If no admin user exists, creates one with the credentials
       defined in the environment variables.

    Returns:
        None
    """
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Initialize the first admin user if it doesn't exist
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if not existing_user:
            hashed_password = get_password_hash(ADMIN_PASSWORD)
            admin_user = User(
                email=ADMIN_EMAIL,
                username=ADMIN_USERNAME,
                password=hashed_password,
                role="admin",
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(
                f"Admin user {ADMIN_USERNAME} created - email: {ADMIN_EMAIL} from .env"
            )
    finally:
        db.close()


def create_tables():
    """
    Create all database tables defined by the SQLAlchemy models.

    This function ensures that all tables defined in the ORM models
    are created in the database if they do not already exist.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)
