# TaskFlow — DevOps Project

A production-oriented task management API used to practice building, deploying, and operating a containerized application with real-world DevOps tools and workflows.

The repository documents the engineering work as the project evolves, including infrastructure decisions, CI/CD, deployment, monitoring, and troubleshooting.

## Project Overview

TaskFlow is a task management application built with FastAPI and PostgreSQL. The application is containerized with Docker and orchestrated locally with Docker Compose.

The deployment uses Nginx as a reverse proxy in front of the API. The API image is built and published to GitHub Container Registry (GHCR) through GitHub Actions. The running environment is reachable remotely through Tailscale.

This is a learning and portfolio project. The infrastructure is production-oriented for practice, but it is not presented as a fully production-hardened service.

## Current Architecture

```text
Client
  |
  | HTTPS over Tailscale
  v
Tailscale Serve
  |
  v
Nginx (port 80)
  |
  | Docker Compose network: api:8000
  v
FastAPI application
  |
  | Docker Compose DNS: db:5432
  v
PostgreSQL 16
  |
  v
Named volume: postgres_data
```

### Services

| Component | Technology | Purpose |
|---|---|---|
| API | FastAPI, Uvicorn, SQLAlchemy, psycopg | Application and task endpoints |
| Database | PostgreSQL 16 | Persistent application data |
| Reverse proxy | Nginx | Routes incoming HTTP requests to the API |
| Containers | Docker | Packages and isolates services |
| Orchestration | Docker Compose | Runs the API, database, and Nginx together |
| CI/CD | GitHub Actions | Runs tests and builds/publishes the container image |
| Image registry | GitHub Container Registry | Stores the TaskFlow API image |
| Remote access | Tailscale Serve | Provides private HTTPS access to the VM service |

## Technology Stack

- **Application:** Python 3.12, FastAPI, Uvicorn
- **Database:** PostgreSQL 16
- **Database access:** SQLAlchemy 2, psycopg
- **Containers:** Docker, Docker Compose
- **Reverse proxy:** Nginx
- **CI/CD:** GitHub Actions
- **Container registry:** GHCR
- **Remote access:** Tailscale

## Repository Structure

```text
.
├── app/
│   ├── routers/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── docker/
│   └── nginx/
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── incidents/
│   └── learning-log/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── requirements.txt
```

## Running the Project

### Prerequisites

- Docker Engine
- Docker Compose plugin
- Git

### 1. Clone the repository

```bash
git clone https://github.com/KuroHakke003/taskflow-devops.git
cd taskflow-devops
```

### 2. Configure environment variables

Create a local `.env` file based on `.env.example` and adjust values if needed.

The Compose deployment uses the database service name `db` as the database hostname. The `.env` file contains local configuration and must not be committed.

### 3. Start the services

```bash
docker compose pull
docker compose up -d
```

### 4. Check service status

```bash
docker compose ps
```

### 5. View application logs

```bash
docker logs api_service
```

The API is exposed to the host through Nginx on port `80`. The API container itself listens on port `8000` internally and is not published directly to the host in the current Compose setup.

Open the API documentation through the host or configured Tailscale URL:

- `/docs` — Swagger UI
- `/openapi.json` — OpenAPI schema

## CI/CD

GitHub Actions is configured to:

1. Run automated tests using Python 3.12 and a PostgreSQL 16 service.
2. Build the TaskFlow Docker image.
3. Authenticate to GitHub Container Registry using `GITHUB_TOKEN`.
4. Publish the image with a `latest` tag and a commit-specific tag.

The deployment Compose configuration uses the published GHCR image rather than building the API image on the VM. Pull the image before recreating or updating the running API container to ensure the latest image is used.

Published image:

```text
ghcr.io/kurohakke003/taskflow-devops:latest
```

## Data Persistence

PostgreSQL stores its data in the named Docker volume `postgres_data`.

- `docker compose down` removes the containers and Compose network but preserves the named volume.
- `docker compose down -v` also removes the Compose-managed named volume and its stored database data.

Use the second command only when intentionally deleting the database volume and its data.

## Monitoring and Operations

The current learning stage includes:

- Inspecting container resource usage with `docker stats`.
- Reviewing API, PostgreSQL, and Nginx logs with `docker logs`.
- Following logs in real time.
- Filtering log output with `grep`.
- Counting matching log lines with `wc -l`.
- Restricting log output to a recent period with `--since`.
- Reproducing a database outage and tracing the resulting API error.

Monitoring, alerting, and production hardening are still evolving parts of the project.

## Project Roadmap

- [x] Linux fundamentals and networking
- [x] Git and GitHub workflow
- [x] Docker and Docker Compose
- [x] CI/CD with GitHub Actions and GHCR
- [x] Deployment and Nginx reverse proxy
- [ ] Monitoring and Operations
- [ ] Cloud infrastructure and Infrastructure as Code
- [ ] Kubernetes
- [ ] Final project hardening and job preparation

## Engineering Documentation

- [Learning Log](docs/learning-log/)
- [Architecture Overview](docs/architecture/overview.md)
- [Architecture Decisions](docs/decisions/)
- [Incident Reports](docs/incidents/)

## Project Goal

The goal is to build practical DevOps experience by operating a real application through its lifecycle: development, testing, containerization, CI/CD, deployment, monitoring, troubleshooting, and infrastructure automation.
