import logging
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from analyzer_2000 import Analyzer


logging.basicConfig(filename="logs.log", level=logging.INFO)

analyzer = Analyzer()

logging.info('Analyzer objects have been created')

class Text(BaseModel):
    text: str
    mode: Optional[str] = 'foreign'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      'http://localhost',
      'http://localhost:8888',
      'http://localhost:8080',
      'http://pushkin-lab.ru',
      'http://pushkin-lab.ru:8888',
      'https://pushkin-lab.ru'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/analyze')
def analyze(text: Text):
    logging.info(text.text)
    if text.mode == 'foreign':
      return analyzer.start_foreign(text.text)
    else:
      return analyzer.start_native(text.text)