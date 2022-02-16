import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from app.analyzer import Analyzer
from app.frequency_check import FrequencyCheck
from fastapi import FastAPI
from pydantic import BaseModel

# prepare logger
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler = TimedRotatingFileHandler("logs/textometr.log", when="D", interval=10)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

analyzer = Analyzer()
logger.info("Analyzer object has been created")

frequencyCheck = FrequencyCheck()
logger.info("Frequency Check object has been created")

class Text(BaseModel):
    text: str
    mode: Optional[str] = "foreign"


app = FastAPI()


@app.post("/analyze")
def analyze(text: Text):
    logger.info(text.text)
    if text.mode == "foreign":
        return analyzer.start_foreign(text.text)
    else:
        return analyzer.start_native(text.text)


@app.post("/frequency")
def analyze(text: Text):
    logger.info(text.text)
    return frequencyCheck.start(text.text)
