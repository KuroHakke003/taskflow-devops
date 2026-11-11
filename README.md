# TaskFlow

A production-oriented task management API used to practice building, deploying, monitoring, and operating a containerized application with real-world DevOps tools and workflows.

The repository documents the engineering work as the project evolves, including infrastructure decisions, CI/CD, deployment, monitoring, observability, and troubleshooting.

This is a hands-on learning and portfolio project focused on understanding how applications and infrastructure behave in real operating environments.

## Project Overview

TaskFlow is a task management application built with FastAPI and PostgreSQL. The application is containerized with Docker and orchestrated locally using Docker Compose.

The deployment uses Nginx as a reverse proxy in front of the API. The API image is built and published to GitHub Container Registry (GHCR) through GitHub Actions.

Remote access is provided through Tailscale Serve, allowing private HTTPS access to the application.

The infrastructure has also been extended with a monitoring stack consisting of Prometheus, Node Exporter, and Grafana. Prometheus collects infrastructure metrics, Node Exporter exposes host-level system metrics, and Grafana provides dashboards and visualization.

The project is continuously evolving as new DevOps concepts and operational practices are introduced.

## Current Architecture

```text
                         Client
                           |
                           | HTTPS
                           v
                     Tailscale Serve
                           |
                           v
                     Nginx (80)
                           |
                           | Docker Compose network
                           v
                     FastAPI (8000)
                           |
                           | Docker DNS: db:5432
                           v
                      PostgreSQL 16
                           |
                           v
                    postgres_data


                  MONITORING STACK

                     Host System
                           |
                           v
                     Node Exporter
                           |
                           | System Metrics
                           v
                       Prometheus
                           |
                           | PromQL / Queries
                           v
                        Grafana
                           |
                           v
                     Dashboards
```

### Services

| Component | Technology | Purpose |
|---|---|---|
| API | FastAPI, Uvicorn, SQLAlchemy, psycopg | Application and task endpoints |
| Database | PostgreSQL 16 | Persistent application data |
| Reverse proxy | Nginx | Routes incoming requests to the API |
| Containers | Docker | Packages and isolates services |
| Orchestration | Docker Compose | Runs application and infrastructure services |
| CI/CD | GitHub Actions | Runs tests and builds/publishes container images |
| Image registry | GitHub Container Registry | Stores the TaskFlow API image |
| Remote access | Tailscale Serve | Provides private HTTPS access |
| Metrics collection | Prometheus | Scrapes and stores monitoring metrics |
| Host monitoring | Node Exporter | Exposes Linux system metrics |
| Visualization | Grafana | Creates dashboards and visualizes metrics |

## Technology Stack

- **Application:** Python 3.12, FastAPI, Uvicorn
- **Database:** PostgreSQL 16
- **Database access:** SQLAlchemy 2, psycopg
- **Containers:** Docker, Docker Compose
- **Reverse proxy:** Nginx
- **CI/CD:** GitHub Actions
- **Container registry:** GHCR
- **Remote access:** Tailscale
- **Monitoring:** Prometheus
- **Metrics exporter:** Node Exporter
- **Visualization:** Grafana
- **Query language:** PromQL

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
│
├── docker/
│   └── nginx/
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── incidents/
│   └── learning-log/
│
├── tests/
│
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

The Compose deployment uses the database service name `db` as the database hostname.

The `.env` file contains local configuration and must not be committed.

### 3. Pull container images

```bash
docker compose pull
```

### 4. Start the services

```bash
docker compose up -d
```

### 5. Check service status

```bash
docker compose ps
```

### 6. View application logs

```bash
docker logs api_service
```

## Application Access

The API is exposed to the host through Nginx on port `80`.

The API container itself listens on port `8000` internally and is not published directly to the host in the current Compose setup.

Available API endpoints:

- `/docs` — Swagger UI
- `/openapi.json` — OpenAPI schema
- `/tasks` — Task management endpoints

Remote access is available through the configured Tailscale Serve HTTPS address.

## CI/CD

GitHub Actions is configured to:

1. Run automated tests using Python 3.12 and a PostgreSQL 16 service.
2. Build the TaskFlow Docker image.
3. Authenticate to GitHub Container Registry using `GITHUB_TOKEN`.
4. Publish the image with a `latest` tag and a commit-specific tag.

The deployment Compose configuration uses the published GHCR image rather than building the API image on the VM.

Pull the image before recreating or updating the running API container to ensure the latest version is used.

Published image:

```text
ghcr.io/kurohakke003/taskflow-devops:latest
```

## Data Persistence

PostgreSQL stores its data in the named Docker volume `postgres_data`.

- `docker compose down` removes containers and the Compose network but preserves named volumes.
- `docker compose down -v` also removes Compose-managed named volumes and their stored database data.

Use the second command only when intentionally deleting the database volume and its contents.

Prometheus uses the named volume `prometheus_data` to retain collected metrics across container recreation.

Grafana stores its application data under `/var/lib/grafana`.

## Monitoring and Observability

The project now includes a monitoring stack built around Prometheus, Node Exporter, and Grafana.

### Prometheus

Prometheus is responsible for collecting and storing time-series metrics from configured targets.

Current learning objectives include:

- Understanding Prometheus architecture and scrape targets.
- Configuring metric collection.
- Understanding time-series data and metric naming.
- Working with PromQL.
- Analyzing metric behavior over time.

### Node Exporter

Node Exporter exposes Linux host-level metrics for Prometheus to scrape.

Metrics currently explored include:

- CPU and system resource information.
- Memory and filesystem metrics.
- Network traffic and interface statistics.
- System uptime and boot time.

Node Exporter runs with access to host-level system information so that metrics describe the VM rather than only its own container.

### Grafana

Grafana is used to visualize metrics collected by Prometheus.

Current learning objectives include:

- Connecting Prometheus as a Grafana data source.
- Understanding dashboard panels.
- Creating metric visualizations.
- Writing PromQL queries for dashboards.
- Interpreting system behavior through graphs.

### PromQL

Queries explored so far include:

- `rate()` — calculating the per-second average rate of increase of a counter over a specified range.
- `time()` — returning the current query evaluation timestamp.
- `node_boot_time_seconds` — identifying the system boot timestamp.
- `node_network_receive_bytes_total` — examining cumulative network traffic received by an interface.

Example query for calculating system uptime:

```promql
time() - node_boot_time_seconds
```

Example query for network traffic:

```promql
rate(node_network_receive_bytes_total[5m])
```

Monitoring and alerting are still evolving parts of the project. The current implementation focuses primarily on infrastructure metrics and understanding the monitoring pipeline.

## Operations and Troubleshooting

Operational experience gained through the project includes:

- Inspecting container resource usage with `docker stats`.
- Reviewing API, PostgreSQL, and Nginx logs with `docker logs`.
- Following logs in real time.
- Filtering log output with `grep`.
- Counting matching log lines with `wc -l`.
- Restricting log output to a recent period with `--since`.
- Investigating database connectivity failures.
- Reproducing database outages and observing application behavior.
- Understanding Docker Compose networking and internal DNS resolution.
- Monitoring host-level metrics with Prometheus and Node Exporter.
- Visualizing infrastructure metrics with Grafana.
- Investigating system uptime and network traffic through PromQL.

The project emphasizes not only deploying services but also understanding failures, identifying their causes, and observing how infrastructure behaves under different conditions.

## Project Roadmap

- [x] Linux fundamentals and networking
- [x] Git and GitHub workflow
- [x] Docker and Docker Compose
- [x] CI/CD with GitHub Actions and GHCR
- [x] Deployment and Nginx reverse proxy
- [x] Initial monitoring stack with Prometheus, Node Exporter, and Grafana
- [ ] Advanced PromQL and custom Grafana dashboards
- [ ] Alerting and monitoring improvements
- [ ] Cloud infrastructure and Infrastructure as Code
- [ ] Kubernetes
- [ ] Final project hardening and job preparation

## Engineering Documentation

Project documentation is maintained alongside the implementation.

- [Learning Log](docs/learning-log/)
- [Architecture Overview](docs/architecture/overview.md)
- [Architecture Decisions](docs/decisions/)
- [Incident Reports](docs/incidents/)

The learning log records practical tasks, technical discoveries, problems encountered, and solutions implemented during development.

## Project Goal

The goal is to build practical DevOps experience by operating a real application through its lifecycle:

**Development → Testing → Containerization → CI/CD → Deployment → Monitoring → Troubleshooting → Infrastructure Automation**

TaskFlow serves as a continuously evolving portfolio project demonstrating practical knowledge of Linux, networking, containers, CI/CD, monitoring, observability, and infrastructure operations.
