# Textometr

Textometr provides information about complexity level and other pedagogical statistics for any given text in Russian.

[![GitHub Super-Linter](https://github.com/leshkin/textometr/workflows/Super-Linter/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Run application in the development mode using Docker

1. Run

   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

2. Open <http://localhost:8080>

## Backend installation, testing and running

1. Go to `backend` folder

2. Create virtual environment

   ```bash
   python3 -m venv env
   ```

3. Activate venv

   ```bash
   source env/bin/activate
   ```

4. Install packages

   ```bash
   pip install -r requirements.txt
   python -m nltk.downloader punkt
   ```

5. Run tests local or inside Docker container

   ```bash
   python3 -m unittest
   ```

6. Run using Uvicorn

   ```bash
   cd app
   uvicorn app.main:app --reload
   ```

7. Deactivate venv
   ```bash
   deactivate
   ```

## Frontend

1. Generate icons
   ```bash
   cd work
   npx vue-pwa-asset-generator -a logo.svg -o output
   ```

## Load Testing

1. Install Artillery

   ```bash
   npm install -g artillery
   ```

2. Run load test
   ```bash
   cd load-tests
   artillery run artillery-load-test.yaml
   ```

## Production

### Deploy app stack in Docker Swarm

1. Build image for frontend
   ```bash
   cd frontend # from the project directory
   docker build -t 1eshkin/textometr-frontend:x.x.x .
   ```
2. Push frontend image to the Docker Hub
   ```bash
   docker push 1eshkin/textometr-frontend:x.x.x
   ```
3. Build image for backend
   ```bash
   cd backend # from the project directory
   docker build -t 1eshkin/textometr-backend:x.x.x .
   ```
4. Push backend image to the Docker Hub
   ```bash
   docker push 1eshkin/textometr-backend:x.x.x
   ```
5. Copy `docker-compose.yml` to the `textometr` folder on remote server

6. Create Docker Swarm on the remote server
   ```bash
   docker swarm init
   ```
7. Run Docker Compose script for building images
   ```bash
   docker-compose up
   ```
   Then Ctrl+C to shutdown
8. Deploy services to Docker Swarm

   ```bash
   docker stack deploy --compose-file docker-compose.yml textometr
   ```

9. Watch running services

   ```bash
   docker service ls # to view active replicas
   docker stats # to monitor resource usage
   ```

### Update stack in Docker Swarm

1. Copy `docker-compose.yml` to the `textometr` folder on remote server

2. Deploy app stack in Docker Swarm

   ```bash
   cd textometr
   docker stack deploy --compose-file docker-compose.yml textometr
   ```

3. Reload nginx config

   ```bash
   docker container exec <container> nginx -s reload
   ```

4. View service logs

   ```bash
   docker service ps --no-trunc textometr_backend
   ```
