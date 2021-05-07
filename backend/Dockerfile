FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app/app
COPY ./data /app/data

RUN pip install --no-cache-dir \
  numpy==1.19.4 \
  scipy==1.5.4 \
  pandas==1.1.4 \
  nltk==3.5 \
  scikit-learn==0.23.2 \
  pymystem3==0.2.0 \
  joblib==0.17 \
  && python -m nltk.downloader punkt