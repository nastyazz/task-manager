FROM python:3.12-slim

WORKDIR /app

RUN pip3 install --upgrade poetry==1.8.3

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app
ENTRYPOINT []

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
