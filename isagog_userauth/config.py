""" import secrets"""

import os

from dotenv import load_dotenv

load_dotenv()

BCRYPT_PEPPER = os.getenv("BCRYPT_PEPPER", "your_pepper_here")
JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key")
ACCESS_TOKEN_LIFETIME = int(os.getenv("ACCESS_TOKEN_LIFETIME", "15"))  # in MINUTES
REFRESH_TOKEN_LIFETIME = int(os.getenv("REFRESH_TOKEN_LIFETIME", "7"))  # in DAYS
