# Isagog user management

<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi" alt="FastAPI" style="margin-right: 10px;"/>
  </a>
  <a href="https://oauth.net/2/" target="_blank">
    <img src="https://img.shields.io/badge/OAuth2-00BFFF?logo=oauth" alt="OAuth2" style="margin-right: 10px;"/>
  </a>
  <a href="https://www.sqlalchemy.org/" target="_blank">
    <img src="https://img.shields.io/badge/SQLAlchemy-100000?logo=sqlalchemy" alt="SQLAlchemy" style="margin-right: 10px;"/>
  </a>
  <a href="https://www.sqlite.org/index.html" target="_blank">
    <img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite" alt="SQLite" style="margin-right: 10px;"/>
  </a>
  <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python" alt="Python" style="margin-right: 10px;"/>
  </a>
  <a href="https://docs.pytest.org/en/stable/" target="_blank">
    <img src="https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest" alt="Pytest" style="margin-right: 10px;"/>
  </a>
  <a href="https://www.docker.com/" target="_blank">
    <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker" alt="Docker" style="margin-right: 10px;"/>
  </a>
  <a href="https://github.com/features/actions" target="_blank">
    <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions" alt="GitHub Actions" style="margin-right: 10px;"/>
  </a>
</p>

Welcome to our project! This project uses FastAPI for user management, login, and authorization.

It implements OAuth2 using bcrypt peppered hashes and issues access and refresh JWT tokens. These
tokens are used to protect your FastAPI application routes via the Dependency mechanism.

It lets you define two classes of users: admin and basic. The latter can only login and refresh
its token, while an admin can create, list, update and delete any other user.

## Getting Started

To get started with this project, follow these steps:

1. **Copy the .env.example file**: Rename the `.env.example` file to `.env`.

2. **Fill in the secrets**: Open the `.env` file and replace the placeholders with your actual secrets. Make sure to keep the secrets protected by double quotes.

3. **Generate encryption keys**: If needed, you can use the `utils/gencrypt.py` program to help you with filling the .env variables

## Important Notes

- Both the email and the username must be unique.
- You can login with either the email or the username.
- You can view the OpenAPI documentation at `host:8000/docs`.

## Usage

The `main.py` file is a demo of how you can import, initialize, and use the user management, login, and authorization in your own FastAPI app.

To be usable you need to have a `.env` file in the project root with the following content:

```
BCRYPT_PEPPER = "yourcomplexpepper"
JWT_SECRET = "yourcomplex JWT secret"
ADMIN_PASSWORD=adminpasswordisverysecretmyfriend
ADMIN_EMAIL=admin@isagog.com
ADMIN_USERNAME=admin
ACCESS_TOKEN_LIFETIME = 15
REFRESH_TOKEN_LIFETIME = 7
USER_DB_URL="sqlite:///./users.db"
USER_TABLE_NAME=users
```

and of course you will customize at least the first three, and better yet the first five values.

## Building the Docker image

You can use the `Makefile` by running `make build` to build an image with the version number specified in the Makefile.
This image is built to be run under a non privileged `isagog` user. `make run` if you want to run this image as is.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
