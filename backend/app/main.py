import logging
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from analyzer_2000 import Analyzer

logging.basicConfig(filename="logs.log", level=logging.INFO)

analyzer = Analyzer()

logging.info('Analyzer objects have been created')

class Text(BaseModel):
    text: str
    mode: Optional[str] = 'foreign'

app = FastAPI()

@app.post('/analyze')
def analyze(text: Text):
    logging.info(text.text)
    if text.mode == 'foreign':
      return analyzer.start_foreign(text.text)
    else:
      return analyzer.start_native(text.text)