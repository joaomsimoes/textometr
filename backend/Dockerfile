FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt