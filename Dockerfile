FROM python:3.14-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../pyproject.toml ../poetry.lock* ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY ../app ./app
COPY ../alembic.ini ./
COPY ../migration ./migration

CMD ["sh", "-c", "until pg_isready -h db -p 5432 -U user; do echo 'Waiting for database...'; sleep 2; done && alembic revision --autogenerate && alembic upgrade head && uvicorn app.api.main:create_app --factory --host 0.0.0.0 --port 8000"]