# Textometr
Textometr allows you to quickly obtain information about a text that is relevant for its preparation for a Russian lesson: the level of complexity of the text, key and most useful words, statistics on the occurrence of words in lexical minimums.

## Backend Installation
1. Go to `backend` folder

2. Install Python 3 and pip

3. Create virtual environment
   ```bash
   python3 -m venv env
   ```

4. Activate venv
   ```bash
   source env/bin/activate
   ```

5. Deactivate venv
   ```bash
   deactivate
   ```

6. Install packages
   ```bash
   pip3 install -r requirements.txt
   python3 -m nltk.downloader punkt
   ```

## Run

1. Command
   ```
   export FLASK_APP=app.py
   flask run
   ```

## Docker

1. Start
   ```bash
   docker-compose up
   ```

2. Go to URL http://localhost:9001/

## Development in Docker

1. Run bash inside Docker container
   ```bash
   docker exec -it CONTAINER_NAME bash
   ```

2. Run tests local or inside Docker container
   ```bash
   python3 -m unittest
   ```
## Production

1. Start
   ```bash
   docker-compose up -d
   ```
2. Stop
   ```bash
   docker stop CONTAINER_NAME
   ```