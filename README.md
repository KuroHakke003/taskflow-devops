# TaskFlow

A production-oriented task management API used to practice building, deploying, monitoring, and operating a containerized application with real-world DevOps tools and workflows.

The repository documents the engineering work as the project evolves, including infrastructure decisions, CI/CD, deployment, monitoring, observability, Kubernetes, and incident troubleshooting.

This is a hands-on learning and portfolio project focused on understanding how applications and infrastructure behave in real operating environments.

## Project Overview

TaskFlow is a task management application built with FastAPI and PostgreSQL.

The primary application deployment uses Docker and Docker Compose, with Nginx acting as a reverse proxy in front of the API. The API image is built and published to GitHub Container Registry (GHCR) through GitHub Actions.

Remote access is provided through Tailscale Serve, allowing private HTTPS access to the application.

The project also includes a dedicated monitoring stack built with Prometheus, Node Exporter, Alertmanager, and Grafana. It collects infrastructure metrics, visualizes system performance, and sends alert notifications to Telegram.

Additionally, the project has been extended with a Kubernetes environment using K3s. This environment is used to learn Kubernetes deployments, services, secrets, persistent storage, container orchestration, and troubleshooting.

The project is continuously evolving as new DevOps concepts and operational practices are introduced.

## Current Architecture

### Docker Compose Application

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
```

### Monitoring Stack

```text
                       Host System
                           |
                           v
                      Node Exporter
                           |
                           | System Metrics
                           v
                       Prometheus
                           |
                  +--------+--------+
                  |                 |
                  v                 v
               Grafana          Alertmanager
                  |                 |
                  v                 v
              Dashboards        Telegram Alerts
```

### Kubernetes Environment (K3s)

```text
                       K3s Cluster
                           |
                           v
                       Namespace
                        taskflow
                           |
              +------------+------------+
              |                         |
              v                         v
        TaskFlow API               PostgreSQL
         Deployment                Deployment
              |                         |
              v                         v
        API Service                 db Service
                                        |
                                        v
                                 PostgreSQL Pod
                                        |
                                        v
                                  postgres-pvc
                                        |
                                        v
                                Persistent Storage
```

The Kubernetes environment is currently experimental and under development. The initial deployments and persistent storage configuration have been created, but PostgreSQL startup troubleshooting remains in progress.

### Services

| Component | Technology | Purpose |
|---|---|---|
| API | FastAPI, Uvicorn, SQLAlchemy, psycopg | Application and task endpoints |
| Database | PostgreSQL 16 | Persistent application data |
| Reverse proxy | Nginx | Routes incoming requests to the API |
| Containers | Docker | Packages and isolates services |
| Application orchestration | Docker Compose | Runs application and infrastructure services |
| Kubernetes | K3s | Local Kubernetes environment |
| Kubernetes workloads | Deployments, Services, Secrets | Manages application and database workloads |
| Persistent storage | PersistentVolumeClaims | Provides persistent storage to Kubernetes workloads |
| CI/CD | GitHub Actions | Runs tests and builds/publishes container images |
| Image registry | GitHub Container Registry | Stores the TaskFlow API image |
| Remote access | Tailscale Serve | Provides private HTTPS access |
| Metrics collection | Prometheus | Scrapes and stores monitoring metrics |
| Host monitoring | Node Exporter | Exposes Linux system metrics |
| Alerting | Alertmanager | Handles monitoring alerts |
| Notifications | Telegram | Delivers alert notifications |
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
- **Kubernetes:** K3s, kubectl
- **Monitoring:** Prometheus
- **Metrics exporter:** Node Exporter
- **Visualization:** Grafana
- **Alerting:** Alertmanager
- **Notifications:** Telegram
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
├── k8s/
│   ├── deployment.yaml
│   ├── postgres-deployment.yaml
│   └── ...
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

The `k8s/` directory contains Kubernetes manifests used to configure the experimental K3s environment.

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

The Docker Compose PostgreSQL service stores its data in the named Docker volume `postgres_data`.

- `docker compose down` removes containers and the Compose network but preserves named volumes.
- `docker compose down -v` also removes Compose-managed named volumes and their stored database data.

Use the second command only when intentionally deleting the database volume and its contents.

Prometheus uses the named volume `prometheus_data` to retain collected metrics across container recreation.

Grafana stores its application data under `/var/lib/grafana`.

The Kubernetes environment uses a PersistentVolumeClaim named `postgres-pvc` for PostgreSQL storage.

The PVC is currently bound to a persistent volume through the K3s `local-path` StorageClass. It has been retained during troubleshooting.

Persistent storage resources should not be deleted during routine troubleshooting because doing so may result in data loss.

## Monitoring and Observability

The project includes a monitoring stack built around Prometheus, Node Exporter, Alertmanager, Grafana, and Telegram notifications.

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

The initial monitoring dashboard has been completed with infrastructure graphs.

The dashboard includes visualizations for:

- CPU usage.
- RAM usage.
- Disk usage.
- Host resource utilization over time.

Grafana is used to identify abnormal resource consumption and understand system behavior through metric visualization.

### Alertmanager and Telegram

Alertmanager handles monitoring alerts and delivers notifications to Telegram.

The project includes a `HighCPUUsage` alert that detects unusually high CPU consumption.

A successful Telegram notification confirmed that the alert delivery pipeline was operational during the November 16 incident.

The monitoring stack has therefore been tested not only through dashboards but also through an actual infrastructure incident.

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

Monitoring and alerting are continuously evolving parts of the project.

## Kubernetes and Container Orchestration

The project has an experimental Kubernetes environment running on K3s.

The purpose of this environment is to understand how application workloads are deployed and operated using Kubernetes resources.

Concepts explored so far:

- K3s cluster initialization.
- Kubernetes nodes and cluster status.
- Namespaces.
- Deployments and Pods.
- Services and internal cluster networking.
- Kubernetes Secrets.
- PersistentVolumeClaims.
- Container resource monitoring.
- Application and database troubleshooting.

### Current Kubernetes Status

Initial TaskFlow API and PostgreSQL deployments have been configured.

The PostgreSQL Deployment uses:

- PostgreSQL 16.
- Kubernetes Secret `postgres-secret`.
- PersistentVolumeClaim `postgres-pvc`.
- A Kubernetes Service named `db`.

However, PostgreSQL has experienced a startup failure. The Pod reported `Running`, but the database did not become available.

The K3s service was temporarily stopped during incident investigation. The PostgreSQL PVC and Kubernetes manifests were retained.

Kubernetes troubleshooting is ongoing, and the environment should not yet be considered a completed production deployment.

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
- Inspecting Linux processes using `htop` and `ps`.
- Understanding process IDs, parent process IDs, process states, and CPU consumption.
- Investigating container runtime processes and `containerd-shim-runc-v2`.
- Troubleshooting Kubernetes Pods and container startup failures.

### Incident: High CPU Usage — November 16, 2026

During Kubernetes troubleshooting, the Grafana dashboard reported CPU usage of approximately 99.9%.

Alertmanager successfully delivered a `HighCPUUsage` notification to Telegram.

Stopping K3s did not immediately resolve the high CPU usage.

Further investigation using `htop` revealed four runaway `gosu postgres` processes, each consuming approximately 200% CPU.

Using `ps`, their shared parent process was identified as `containerd-shim-runc-v2`, associated with the Kubernetes container runtime.

The four processes continued running even after the K3s service had been stopped.

After terminating the processes, CPU utilization dropped significantly:

| Metric | Before | After |
|---|---:|---:|
| CPU 0 | 100% | 2.8% |
| CPU 1 | 100% | 0.8% |
| Load average (1 min) | 5.04 | 3.87 |
| RAM | 927 MB | 893 MB |

This confirmed that the four runaway processes were responsible for the immediate CPU overload.

The underlying reason why the processes became stuck remains under investigation.

The incident provided practical experience with monitoring alerts, Linux process inspection, container runtime behavior, and resource troubleshooting.

The project emphasizes not only deploying services but also understanding failures, identifying their causes, and observing how infrastructure behaves under different conditions.

## Project Roadmap

- [x] Linux fundamentals and networking
- [x] Git and GitHub workflow
- [x] Docker and Docker Compose
- [x] CI/CD with GitHub Actions and GHCR
- [x] Deployment and Nginx reverse proxy
- [x] Initial monitoring stack with Prometheus and Node Exporter
- [x] Grafana dashboard with infrastructure graphs
- [x] Alertmanager and Telegram alert notifications
- [x] Initial K3s cluster setup and Kubernetes resource configuration
- [ ] Complete Kubernetes deployment and troubleshooting
- [ ] Restore PostgreSQL availability in Kubernetes
- [ ] Advanced PromQL and monitoring improvements
- [ ] Cloud infrastructure and Infrastructure as Code
- [ ] Terraform
- [ ] Further Kubernetes practice
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

TaskFlow serves as a continuously evolving portfolio project demonstrating practical knowledge of Linux, networking, containers, CI/CD, monitoring, observability, Kubernetes, and infrastructure operations.
