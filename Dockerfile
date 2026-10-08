# Official Python images publish amd64 and arm64. Build on the VM, or in CI
# with --platform set to the VM architecture, so the image can run there.
# The app user is uid 1000. The host media directory must be writable by that user.

FROM python:3.13-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv \
    && pip install "poetry==${POETRY_VERSION}"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-ansi \
    && pip uninstall -y poetry


FROM python:3.13-slim-bookworm AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=base /opt/venv /opt/venv
COPY --chown=app:app . .
RUN mkdir -p media staticfiles \
    && chown app:app media staticfiles

USER app
EXPOSE 8000
CMD ["gunicorn", "django_store.wsgi:application", "--bind", "0.0.0.0:8000"]
