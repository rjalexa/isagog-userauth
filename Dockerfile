FROM thehale/python-poetry:1.8.3-py3.11-slim as base
RUN groupadd -r isagog && useradd -r -g isagog isagog

WORKDIR /userauth
COPY poetry.lock pyproject.toml /userauth/
RUN poetry install --no-root

FROM base as application
WORKDIR /userauth
COPY .env .
RUN chown -R isagog:isagog .env
COPY isagog_userauth/*.py .
RUN chown -R isagog:isagog /userauth
COPY userauth/routers/user.py ./routers/
RUN chown -R isagog:isagog /userauth/routers/

ENV PYTHONPATH=/userauth
USER isagog
EXPOSE 8000