import logging
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import analyzer_foreign
import analyzer_native

logging.basicConfig(filename="logs.log", level=logging.INFO)

foreign = analyzer_foreign.Analyzer_foreign()
native = analyzer_native.Analyzer_native()

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
      return foreign.start(text.text)
    else:
      return native.start(text.text)