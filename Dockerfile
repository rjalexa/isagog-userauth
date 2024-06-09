# Base stage
FROM thehale/python-poetry:1.8.3-py3.11-slim as base
RUN groupadd -r isagog && useradd -r -g isagog isagog

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install --no-root --with dev; else poetry install --no-root; fi

# Application stage
FROM base as application
WORKDIR /app
COPY .env .
RUN chown -R isagog:isagog .env
COPY isagog_userauth /app/isagog_userauth
RUN chown -R isagog:isagog /app/isagog_userauth
COPY isagog_userauth/routers /app/isagog_userauth/routers
RUN chown -R isagog:isagog /app/isagog_userauth/routers

# Ensure the /app directory itself is writable by isagog
# needed to create user.db at runtime
RUN chown isagog:isagog /app

ENV PYTHONPATH=/app
USER isagog
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "isagog_userauth.main:app", "--host", "0.0.0.0", "--port", "8000"]
