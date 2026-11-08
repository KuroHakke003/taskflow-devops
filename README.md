# TaskFlow

**A task management API and hands-on DevOps engineering project.**

TaskFlow is a task management application built to explore real-world software development, containerization, CI/CD automation, and infrastructure engineering.

The project focuses on building a reliable application and developing the infrastructure and automation practices required to build, test, package, deploy, and operate it.

## About the Project

TaskFlow provides a REST API for managing tasks, with PostgreSQL as its persistent database.

The application is built with FastAPI and SQLAlchemy and runs in Docker containers alongside PostgreSQL.

Beyond application development, TaskFlow serves as a practical DevOps learning project covering the entire application lifecycle — from local development and containerization to automated testing and image publishing.

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python 3.12, FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2 |
| Testing | pytest |
| Containers | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry (GHCR) |
| Web Server / Reverse Proxy | Nginx |
| Operating System | Ubuntu Linux |
| Version Control | Git, GitHub |

## Architecture

The current application consists of two main services:

- **API** — FastAPI application responsible for handling HTTP requests and application logic.
- **Database** — PostgreSQL service responsible for persistent data storage.

Docker Compose manages the services, their networking, configuration, health checks, and persistent storage.

The API communicates with PostgreSQL through Docker's internal service network.

## CI/CD Pipeline

TaskFlow uses GitHub Actions to automate testing, Docker image building, and publishing.

### Continuous Integration (CI)

The CI workflow:

1. Runs on pushes and pull requests targeting `main`.
2. Creates an Ubuntu runner.
3. Starts a temporary PostgreSQL 16 service container.
4. Sets up Python 3.12 and installs dependencies.
5. Executes automated tests using pytest.

### Continuous Delivery (CD)

The CD workflow:

1. Runs automated tests before building the image.
2. Authenticates with GitHub Container Registry using `GITHUB_TOKEN`.
3. Builds the Docker image using the repository's Dockerfile.
4. Publishes the image to GHCR after successful tests.

Images are published with two tags:

- `latest` — a convenient reference to the latest published image.
- Git commit SHA — identifies the exact source revision used to build the image.

### Published Docker Image

The TaskFlow image is publicly available through GitHub Container Registry:

`ghcr.io/kurohakke003/taskflow-devops`

Pull the image:

```bash
docker pull ghcr.io/kurohakke003/taskflow-devops:latest
```

## Running Locally

### Prerequisites

- Docker Engine
- Docker Compose plugin

### Setup

Clone the repository:

```bash
git clone https://github.com/KuroHakke003/taskflow-devops.git
cd taskflow-devops
```

Create a local environment file:

```bash
cp .env.example .env
```

Start the application:

```bash
docker compose up --build -d
```

The API will be available at:

- **API:** http://localhost:8080
- **Interactive API documentation:** http://localhost:8080/docs

Stop the application:

```bash
docker compose down
```

Docker Compose uses a named volume for PostgreSQL data, so database contents persist when containers are stopped or recreated. Avoid `docker compose down -v` unless you intentionally want to remove the database volume.

**Note:** The credentials provided in `.env.example` are development placeholders and must not be used in production.

## Project Status

<badge color="success">Implemented</badge>

- FastAPI application and REST endpoints
- PostgreSQL integration
- Dockerfile and Docker image
- Docker Compose orchestration
- Environment-based configuration
- PostgreSQL health checks and persistent volumes
- Automated tests with pytest
- GitHub Actions CI workflow
- Automated Docker image publishing to GHCR

<badge color="warning">In Progress</badge>

- Deployment to a Linux server using the published image
- Nginx reverse proxy configuration
- Domain and HTTPS configuration

**Planned:**

- Monitoring, metrics, logging, and alerting
- Backup and recovery procedures
- Cloud infrastructure (AWS)
- Infrastructure as Code (Terraform)
- Configuration management (Ansible)
- Kubernetes orchestration
- Production security and reliability improvements

## Engineering Documentation

Project development and technical decisions are documented in the following directories:

- [Learning Log](docs/learning-log/) — daily learning progress and completed tasks.
- [Architecture](docs/architecture/) — system architecture and technical documentation.
- [Architecture Decisions](docs/decisions/) — important engineering decisions and their rationale.
- [Incident Reports](docs/incidents/) — troubleshooting cases and incident analysis.

## Project Goals

TaskFlow is an evolving engineering project with the following long-term goals:

- Build and maintain a functional backend application.
- Design and document its architecture.
- Develop reliable containerized infrastructure.
- Automate testing, building, and delivery.
- Deploy and operate the application on Linux and cloud infrastructure.
- Implement monitoring, observability, and backup strategies.
- Apply infrastructure automation and security best practices.

---

**This project is actively evolving.** Its infrastructure and documentation are updated as new engineering practices and technologies are implemented.
