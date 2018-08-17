 FROM python:3.7
 ADD . /code
 WORKDIR /code
 RUN pip3 install -r requirements.txt
 RUN python3 -m nltk.downloader punkt