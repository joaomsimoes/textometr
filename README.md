# discover-your-text
Get some information about text.

## Installation

1. Install Python 3 and pip

2. Create virtual environment
   ```bash
   python3 -m venv env
   ```

3. Activate venv
   ```bash
   source env/bin/activate
   ```

4. Deactivate venv
   ```bash
   deactivate
   ```

5. Install packages
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
   python -m unittest tests/tests.py
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