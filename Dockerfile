# Base stage
FROM thehale/python-poetry:1.8.3-py3.11-slim as base
RUN groupadd -r isagog && useradd -r -g isagog isagog

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install --no-root --with dev; else poetry install --no-root; fi

# Test stage
FROM base as test
WORKDIR /app
COPY . .
RUN poetry install --no-root --with dev

# Production stage
FROM base as production
WORKDIR /app
COPY . .
RUN poetry install --no-root --no-dev

COPY --chown=isagog:isagog isagog_userauth /app/isagog_userauth
COPY --chown=isagog:isagog isagog_userauth/routers /app/isagog_userauth/routers
COPY --chown=isagog:isagog .env .

ENV PYTHONPATH=/app
USER isagog
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "isagog_userauth.main:app", "--host", "0.0.0.0", "--port", "8000"]
