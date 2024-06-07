""" small utility function to generate pepper and jwt secret"""

import secrets
import string


def generate_pepper(length=32):
    """gen pepper"""
    # Define the alphabet for the pepper string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Generate a secure random string of the specified length
    pepper = "".join(secrets.choice(alphabet) for _ in range(length))
    return pepper


def generate_jwt_secret(length=64):
    """gen JWT secret"""
    # Define the alphabet for the JWT secret
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Generate a secure random string of the specified length
    jwt_secret = "".join(secrets.choice(alphabet) for _ in range(length))
    return jwt_secret


# Generate a 64-character long JWT secret
strong_jwt_secret = generate_jwt_secret()
print(f"Here's your JWT secret: {strong_jwt_secret}")

# Generate a 32-character long pepper string
complex_pepper = generate_pepper()
print(f"Here's your pepper: {complex_pepper}")
