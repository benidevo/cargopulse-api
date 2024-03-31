ARG PYTHON_VERSION=3.11.2-slim-bullseye
FROM python:${PYTHON_VERSION} as base

FROM base as python-build-stage
ARG BUILD_ENVIRONMENT=dev

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY ./requirements /tmp/requirements

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r /tmp/requirements/${BUILD_ENVIRONMENT}.txt

FROM base as python-run-stage
ARG BUILD_ENVIRONMENT=dev
ARG APP_HOME=/app/src

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat \
 && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./src ${APP_HOME}

COPY ./docker/dev/entrypoint /entrypoint
RUN sed -i 's/\r//g' /entrypoint \
 && chmod +x /entrypoint

CMD ["/entrypoint"]
