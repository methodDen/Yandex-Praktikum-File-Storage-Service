FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    COLUMNS=200 \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    libpq-dev \
    gettext \
    cmake \
    ffmpeg \
    libsm6 \
    libxext6 \
    curl \
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version

COPY ./pyproject.toml ./poetry.lock ./

WORKDIR /src

RUN poetry run pip install -U pip && poetry install

COPY ./ ./

COPY entrypoint.sh ./

RUN chmod +x './entrypoint.sh'

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/src"

CMD ["./entrypoint.sh"]