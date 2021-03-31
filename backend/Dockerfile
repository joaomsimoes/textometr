FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app/app
COPY ./data /app/data
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt