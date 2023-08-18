# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install poetry 
RUN poetry config installer.max-workers 10

RUN poetry install --no-root --no-directory

COPY ./src/front ./front
RUN poetry install --only main

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "front/app.py", "--server.port=8501", "--server.address=0.0.0.0"]