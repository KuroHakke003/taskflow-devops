# TaskFlow

A production-oriented task management API used to practice building, deploying, monitoring, and operating a containerized application with real-world DevOps tools and workflows.

The repository documents the engineering work as the project evolves, including infrastructure decisions, CI/CD, deployment, monitoring, observability, Kubernetes, security hardening, and incident troubleshooting.

This is a hands-on learning and portfolio project focused on understanding how applications and infrastructure behave in real operating environments.

## Project Overview

TaskFlow is a task management application built with FastAPI and PostgreSQL.

The primary application deployment uses Docker and Docker Compose, with Nginx acting as a reverse proxy in front of the API. The API image is built and published to GitHub Container Registry (GHCR) through GitHub Actions.

Remote access is provided through Tailscale Serve, allowing private HTTPS access to the application.

The project also includes a dedicated monitoring stack built with Prometheus, Node Exporter, Alertmanager, and Grafana. It collects infrastructure metrics, visualizes system performance, and sends alert notifications to Telegram.

Additionally, the project includes a Kubernetes environment running on K3s. It is used to practice workload orchestration, service discovery, configuration management, persistent storage, autoscaling, security controls, network isolation, and troubleshooting.

The project is continuously evolving as new DevOps concepts and operational practices are introduced.

## Current Architecture

### Docker Compose Application

```text
                          Client
                            |
                          HTTPS
                            |
                      Tailscale Serve
                            |
                          Nginx (80)
                            |
                     Docker Compose Network
                            |
                        FastAPI (8000)
                            |
                       Docker DNS: db
                            |
                       PostgreSQL 16
                            |
                        postgres_data
```

### Monitoring Stack

```text
                         Host System
                            |
                       Node Exporter
                            |
                      System Metrics
                            |
                         Prometheus
                            |
                    +--------+--------+
                    |                 |
                 Grafana         Alertmanager
                    |                 |
                Dashboards      Telegram Alerts
```

### Kubernetes Environment (K3s)

```text
                         K3s Cluster
                            |
                      Namespace: taskflow
                            |
                   +----------+----------+
                   |                     |
                   v                     v
              TaskFlow API           PostgreSQL
               Deployment            StatefulSet
               (2 replicas)          (1 replica)
                   |                     |
                   v                     v
              API Service          Headless Service
                   |                     |
                   |                 postgres-0
                   |                     |
                   |                  postgres-pvc
                   |
              API NetworkPolicy
                   |
        Ingress allowed from Pods
        within namespace taskflow

PostgreSQL NetworkPolicy:
Ingress allowed to TCP/5432
from TaskFlow API Pods only
```

The Kubernetes environment is a separate deployment from Docker Compose. Both environments have their own application workloads and database storage.

The API communicates with PostgreSQL through the Kubernetes Service named `db`.

The PostgreSQL StatefulSet uses a headless Service for stable network identity and a PersistentVolumeClaim for persistent storage.

NetworkPolicies restrict incoming traffic to the API and PostgreSQL workloads.

### Services

| Component | Technology | Purpose |
|---|---|---|
| API | FastAPI, Uvicorn, SQLAlchemy, psycopg | Application and task endpoints |
| Database | PostgreSQL 16 | Persistent application data |
| Reverse proxy | Nginx | Routes incoming requests to the API |
| Containers | Docker | Packages and isolates services |
| Application orchestration | Docker Compose | Runs application and infrastructure services |
| Kubernetes | K3s | Local Kubernetes environment |
| Workload management | Deployments, StatefulSets, Pods | Manages application and database workloads |
| Networking | Kubernetes Services, NetworkPolicies | Internal service discovery, communication, and ingress restrictions |
| Configuration | ConfigMaps | Stores non-sensitive application configuration |
| Secrets | Kubernetes Secrets | Stores database credentials |
| Persistent storage | PersistentVolumeClaims | Provides persistent storage to Kubernetes workloads |
| Autoscaling | Horizontal Pod Autoscaler | Scales API replicas based on CPU and memory utilization |
| Container security | SecurityContext | Restricts container privileges and execution identity |
| Kubernetes identity | ServiceAccount | Provides a dedicated workload identity |
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
- **Kubernetes workloads:** Deployments, StatefulSets, Pods
- **Kubernetes networking:** ClusterIP Services, Headless Services, NetworkPolicies
- **Kubernetes configuration:** ConfigMaps, Secrets
- **Kubernetes security:** SecurityContext, ServiceAccounts, RBAC principles
- **Persistent storage:** PersistentVolumes, PersistentVolumeClaims, local-path
- **Autoscaling:** Horizontal Pod Autoscaler (HPA)
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
│   ├── api-service.yaml
│   ├── configmap.yaml
│   ├── hpa.yaml
│   ├── postgres-statefulset.yaml
│   ├── postgres-service.yaml
│   ├── postgres-headless.yaml
│   ├── postgres-pvc.yaml
│   ├── serviceaccount.yaml
│   ├── networkpolicy-postgres.yaml
│   └── networkpolicy-api.yaml
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

The `k8s/` directory contains Kubernetes manifests used to configure the K3s environment.

Sensitive configuration files, including database credentials, are intentionally excluded from version control.

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

The Docker Compose API is exposed to the host through Nginx on port `80`.

The API container itself listens on port `8000` internally and is not published directly to the host in the current Compose setup.

Available API endpoints:

- `/docs` — Swagger UI
- `/openapi.json` — OpenAPI schema
- `/tasks` — Task management endpoints
- `/health/live` — Kubernetes liveness check
- `/health/ready` — Kubernetes readiness check

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

### Kubernetes Storage

The Kubernetes PostgreSQL workload uses a PersistentVolumeClaim named `postgres-pvc`.

- Storage request: `2Gi`
- Access mode: `ReadWriteOnce`
- Storage class: K3s `local-path`
- Status: `Bound`

The PVC is used by the PostgreSQL StatefulSet. Persistent storage resources should not be deleted during routine troubleshooting because doing so may result in data loss.

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

Metrics explored include:

- CPU and system resource information.
- Memory and filesystem metrics.
- Network traffic and interface statistics.
- System uptime and boot time.

Node Exporter runs with access to host-level system information so that metrics describe the VM rather than only its own container.

### Grafana

Grafana is used to visualize metrics collected by Prometheus.

The monitoring dashboard includes visualizations for:

- CPU usage.
- RAM usage.
- Disk usage.
- Host resource utilization over time.

Grafana helps identify abnormal resource consumption and understand system behavior through metric visualization.

### Alertmanager and Telegram

Alertmanager handles monitoring alerts and delivers notifications to Telegram.

The project includes a `HighCPUUsage` alert that detects unusually high CPU consumption.

A successful Telegram notification confirmed that the alert delivery pipeline was operational during the November 16 incident.

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

The project includes a Kubernetes environment running on K3s.

The purpose of this environment is to understand how application workloads are deployed, configured, secured, scaled, and operated using Kubernetes resources.

### Kubernetes Concepts Implemented

- K3s cluster initialization and node inspection.
- Namespaces.
- Pods and Deployments.
- ClusterIP Services and internal DNS.
- Headless Services.
- ConfigMaps and Secrets.
- PersistentVolumes and PersistentVolumeClaims.
- Liveness and readiness probes.
- CPU and memory requests and limits.
- Metrics API and resource monitoring with `kubectl top`.
- Horizontal Pod Autoscaler (HPA).
- PostgreSQL StatefulSet.
- PostgreSQL backup and restore testing.
- ServiceAccounts and token mount control.
- RBAC and least-privilege principles.
- Container and Pod security hardening.
- NetworkPolicies and network isolation testing.

### Current Kubernetes Architecture

The cluster uses a dedicated namespace named `taskflow`.

#### TaskFlow API

- Managed by a Deployment named `taskflow-api`.
- Exposed internally through the `taskflow-api` ClusterIP Service.
- Uses a ConfigMap for non-sensitive application configuration.
- Uses a Kubernetes Secret for PostgreSQL credentials.
- Configured with liveness and readiness probes.
- Has CPU and memory requests and limits.
- Runs as a non-root user.
- Uses a dedicated ServiceAccount.
- Does not automatically mount a ServiceAccount token.
- Has privilege escalation disabled and Linux capabilities dropped.
- Scaled through an HPA based on CPU and memory utilization.
- Protected by a NetworkPolicy that restricts ingress to Pods in the same namespace.

#### PostgreSQL

- Managed by a StatefulSet named `postgres`.
- Uses PostgreSQL 16.
- Uses the `postgres-secret` Kubernetes Secret for credentials.
- Uses the `postgres-pvc` PersistentVolumeClaim.
- Uses a headless Service named `postgres-headless` for stable Pod identity.
- Is reachable by the API through the regular `db` ClusterIP Service.
- Has CPU and memory requests and limits.
- Protected by a NetworkPolicy that restricts ingress to TaskFlow API Pods on TCP port `5432`.

### Configuration Management

A ConfigMap named `taskflow-config` stores non-sensitive application settings, including:

- `APP_NAME`
- `APP_ENV`
- `APP_HOST`
- `APP_PORT`

A Secret named `postgres-secret` stores database configuration and credentials:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

The API receives database credentials through Secret references and constructs its database connection URL using environment variable substitution.

Sensitive Secret manifests and credentials are not committed to the repository.

### Health Checks

The API Deployment uses two Kubernetes probes:

- **Liveness probe:** `/health/live` — checks whether the application process is alive.
- **Readiness probe:** `/health/ready` — checks whether the application is ready to receive traffic.

These probes allow Kubernetes to detect unhealthy containers and avoid sending traffic to Pods that are not ready.

### Resource Requests and Limits

CPU and memory resources are configured for both application and database workloads.

| Workload | Resource | Request | Limit |
|---|---|---:|---:|
| TaskFlow API | CPU | 100m | 500m |
| TaskFlow API | Memory | 128Mi | 256Mi |
| PostgreSQL | CPU | 100m | 500m |
| PostgreSQL | Memory | 128Mi | 512Mi |

Requests define the resources Kubernetes uses for scheduling decisions. Limits define the maximum resource consumption allowed for a container.

### Horizontal Pod Autoscaler

The API is configured with a Horizontal Pod Autoscaler named `api-hpa`.

Current configuration:

- Target: Deployment `taskflow-api`
- Minimum replicas: 1
- Maximum replicas: 3
- CPU utilization target: 50% of requested CPU
- Memory utilization target: 70% of requested memory

The HPA uses resource metrics to adjust the number of API replicas based on CPU and memory utilization.

A load test using a temporary BusyBox Pod successfully triggered scale-up from one API replica to the configured maximum of three replicas.

PostgreSQL is not autoscaled by this HPA. The autoscaling configuration applies only to the stateless API workload.

### PostgreSQL StatefulSet

PostgreSQL was migrated from a Deployment to a StatefulSet.

The migration introduced:

- Stable Pod identity (`postgres-0`).
- A dedicated headless Service.
- Stateful workload management.
- Reuse of the existing PersistentVolumeClaim.
- Retention of the existing persistent volume during migration.

The normal `db` Service remains in place, so the API can continue connecting to PostgreSQL through the same service name.

### Backup and Recovery

A PostgreSQL backup was created using `pg_dump` and inspected to verify the resulting SQL dump.

A restore test was performed using a temporary PostgreSQL environment:

- Restored the database dump.
- Verified that the database schema and `tasks` table were present.
- Verified table ownership.
- Confirmed that the restore operation completed successfully.

The backup used for this test represented an empty baseline database, so the restored `tasks` table contained zero rows. The test verified the restoration procedure and schema recovery, not recovery of populated production data.

### ServiceAccount and Access Control

The API uses a dedicated ServiceAccount named `taskflow-api`.

- The Deployment references the dedicated ServiceAccount.
- Automatic ServiceAccount token mounting is disabled.
- The token mount was verified to be absent from the running API Pod.
- The application does not currently require Kubernetes API permissions.
- No additional Role or RoleBinding permissions were granted to the API.

This follows a least-privilege approach by avoiding unnecessary access to the Kubernetes API.

### SecurityContext and Container Hardening

The TaskFlow API container is configured to run with reduced privileges.

- `runAsNonRoot: true`
- `runAsUser: 999`
- `runAsGroup: 999`
- `allowPrivilegeEscalation: false`
- `capabilities.drop: ALL`

The Dockerfile was also modified to run the application as a non-root user. The container's user identity was verified during testing.

### NetworkPolicies

Two NetworkPolicies are configured in the `taskflow` namespace.

**PostgreSQL NetworkPolicy:**

- Selects PostgreSQL Pods using `app=postgres`.
- Allows ingress on TCP port `5432`.
- Allows connections only from Pods labeled `app=taskflow-api` in the same namespace.

**API NetworkPolicy:**

- Selects API Pods using `app=taskflow-api`.
- Allows ingress on TCP port `8000`.
- Allows connections from Pods in the same namespace using an empty `podSelector`.
- Does not restrict egress traffic.

**Network isolation was tested:**

- Verified that an in-namespace test Pod could access the API.
- Verified that a test Pod in another namespace could not access the API through the Service.
- Verified that direct Pod-IP access from the external test namespace was also blocked.
- Tested PostgreSQL ingress from an unauthorized test Pod and confirmed it could not connect.

These tests were performed using temporary Pods and a temporary namespace, which were removed after testing.

### Current Kubernetes Status

| Resource | Name | Status |
|---|---|---|
| Namespace | `taskflow` | Configured |
| API Deployment | `taskflow-api` | 2/2 Ready |
| API Service | `taskflow-api` | Configured |
| PostgreSQL StatefulSet | `postgres` | 1/1 Ready |
| PostgreSQL Pod | `postgres-0` | Running |
| Database Service | `db` | Configured |
| Headless Service | `postgres-headless` | Configured |
| PersistentVolumeClaim | `postgres-pvc` | Bound, 2Gi |
| ConfigMap | `taskflow-config` | Configured |
| Secret | `postgres-secret` | Configured |
| ServiceAccount | `taskflow-api` | Configured |
| Horizontal Pod Autoscaler | `api-hpa` | Active, 2 replicas |
| PostgreSQL NetworkPolicy | `postgres-network-policy` | Applied and tested |
| API NetworkPolicy | `taskflow-api-network-policy` | Applied and tested |

The API and PostgreSQL workloads are running in the `taskflow` namespace. The HPA has been verified through a scale-up test, and the network isolation policies have been tested.

The Kubernetes environment remains a learning and portfolio environment rather than a production-ready deployment.

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
- Troubleshooting Kubernetes Pods, Services, and container startup failures.
- Inspecting Kubernetes resource usage with `kubectl top`.
- Monitoring HPA scaling behavior.
- Working with PostgreSQL StatefulSets and persistent storage.
- Creating and inspecting PostgreSQL backups.
- Testing PostgreSQL restore procedures.
- Testing Kubernetes network isolation.

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

### Incident: Prometheus Instrumentator Compatibility — November 18, 2026

The TaskFlow API returned HTTP 500 errors after a compatibility issue with `prometheus-fastapi-instrumentator` 7.1.0.

The middleware failed with an `AttributeError` involving an internal FastAPI router object.

The dependency constraint was adjusted in `requirements.txt` to avoid the incompatible version.

After rebuilding and deploying the updated image, the API endpoints were verified again.

This incident provided practical experience with dependency compatibility, application logs, error investigation, and CI/CD-based deployment fixes.

The project emphasizes not only deploying services but also understanding failures, identifying their causes, and observing how infrastructure behaves under different conditions.

## Project Roadmap

### Completed

- [x] Linux fundamentals and networking
- [x] Git and GitHub workflow
- [x] Docker and Docker Compose
- [x] CI/CD with GitHub Actions and GHCR
- [x] Deployment and Nginx reverse proxy
- [x] Monitoring stack with Prometheus and Node Exporter
- [x] Grafana dashboard with infrastructure graphs
- [x] Alertmanager and Telegram alert notifications
- [x] Initial K3s cluster setup
- [x] Kubernetes Namespaces, Deployments, Pods, and Services
- [x] ConfigMaps and Secrets
- [x] Persistent storage with PVCs
- [x] Liveness and readiness probes
- [x] CPU and memory requests and limits
- [x] Kubernetes resource monitoring
- [x] Horizontal Pod Autoscaler using CPU and memory
- [x] HPA scale-up testing
- [x] PostgreSQL migration to StatefulSet
- [x] PostgreSQL backup creation and inspection
- [x] PostgreSQL restore testing
- [x] Dockerfile non-root hardening
- [x] Kubernetes SecurityContext
- [x] Dedicated ServiceAccount
- [x] Disabled automatic ServiceAccount token mounting
- [x] RBAC and least-privilege approach
- [x] PostgreSQL NetworkPolicy
- [x] API NetworkPolicy
- [x] Network isolation testing

### Planned

- [ ] Kubernetes Ingress and external routing
- [ ] TLS configuration for Kubernetes workloads
- [ ] Rolling updates and rollbacks
- [ ] Helm charts for TaskFlow
- [ ] Further Kubernetes troubleshooting practice
- [ ] Terraform and Infrastructure as Code
- [ ] Cloud infrastructure deployment
- [ ] Further backup and recovery testing with populated data
- [ ] Final project documentation and job preparation

## Engineering Documentation

Project documentation is maintained alongside the implementation.

- [Learning Log](https://github.com/KuroHakke003/taskflow-devops/blob/main/docs/learning-log)
- [Architecture Overview](https://github.com/KuroHakke003/taskflow-devops/blob/main/docs/architecture/overview.md)
- [Architecture Decisions](https://github.com/KuroHakke003/taskflow-devops/blob/main/docs/decisions)
- [Incident Reports](https://github.com/KuroHakke003/taskflow-devops/blob/main/docs/incidents)

The learning log records practical tasks, technical discoveries, problems encountered, and solutions implemented during development.

## Project Goal

The goal is to build practical DevOps experience by operating a real application through its lifecycle:

**Development → Testing → Containerization → CI/CD → Deployment → Monitoring → Troubleshooting → Infrastructure Automation**

TaskFlow serves as a continuously evolving portfolio project demonstrating practical knowledge of Linux, networking, containers, CI/CD, monitoring, observability, Kubernetes, security hardening, and infrastructure operations.
