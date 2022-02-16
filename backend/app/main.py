import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

import pymystem3
from app.analyzer import Analyzer
from app.frequency_check import FrequencyCheck
from fastapi import FastAPI
from pydantic import BaseModel

# prepare logger
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler = TimedRotatingFileHandler("logs/textometr.log", when="midnight")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)

analyzer = Analyzer(mystem)
logger.info("Analyzer object has been created")

frequencyCheck = FrequencyCheck(mystem)
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
def frequency(text: Text):
    logger.info(text.text)
    return frequencyCheck.start(text.text)
