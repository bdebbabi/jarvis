# app/Dockerfile

FROM python:3.10-slim

RUN apt-get update && apt-get install -y libportaudio2 

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install poetry 
RUN poetry config installer.max-workers 10
RUN poetry install --no-root --no-directory

COPY ./src/back ./back
RUN poetry install --only main

CMD ["poetry", "run", "uvicorn", "back.main:app", "--host", "0.0.0.0", "--port", "80"]