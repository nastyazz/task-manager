FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip3 install --upgrade  poetry==1.8.3

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi  \
    && echo yes | python3 -m poetry cache clear . --all
COPY . /app
CMD ["uvicorn","src.main:create_app","--host","0.0.0.0","--port","8000"]