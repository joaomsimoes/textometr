from analyzer_foreign import Analyzer_foreign
from analyzer_native import Analyzer_native
import logging
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(filename="logs.log", level=logging.INFO)

analyzer_foreign = Analyzer_foreign()
analyzer_native = Analyzer_native()

logging.info('Analyzer objects have been created')

class Text(BaseModel):
    text: str
    mode: Optional[str] = 'foreign'

app = FastAPI()

origins = [
  'http://localhost:8081',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST'],
    allow_headers=['*'],
)

@app.post('/analyze')
def analyze(text: Text):
    logging.info(text.text)
    if text.mode == 'foreign':
      return analyzer_foreign.start(text.text)
    else:
      return analyzer_native.start(text.text)   