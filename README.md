# TaskFlow

A production-oriented task management API used as a hands-on DevOps learning and portfolio project. TaskFlow is used to practice building, containerizing, deploying, securing, monitoring, troubleshooting, and automating an application across Docker Compose and Kubernetes environments.

The project documents practical infrastructure work, engineering decisions, incidents, and lessons learned while progressively building toward cloud infrastructure and Kubernetes deployment in AWS.

## Project Overview

TaskFlow is a task management API built with FastAPI and PostgreSQL.

The project has two deployment environments:

- **Docker Compose:** the API, PostgreSQL and Nginx reverse proxy, with private remote access through Tailscale Serve.
- **K3s:** a Kubernetes deployment with two API replicas, PostgreSQL StatefulSet and persistent storage, Traefik Ingress, TLS, NetworkPolicies, resource management, and autoscaling.

The project also includes monitoring and alerting using Prometheus, Node Exporter, Alertmanager, Grafana and Telegram. A GitHub Actions pipeline now runs tests, builds and publishes Docker images to GHCR, and deploys a specific image revision to K3s over private Tailscale connectivity and restricted SSH.

## Architecture

### Docker Compose

```
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
                      PostgreSQL 16
                           |
                    postgres_data

```

### Monitoring

```
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

### Kubernetes (K3s)

```
                         K3s Cluster
                           |
                    Namespace: taskflow
                           |
                  +--------+---------+
                  |                  |
             TaskFlow API        PostgreSQL
              Deployment          StatefulSet
              (2 replicas)          (1 pod)
                  |                  |
             API Service       db / Headless Service
                  |                  |
              Ingress             postgres-0
              (Traefik)              |
                                  postgres-pvc

       NetworkPolicies restrict workload ingress

```

The Kubernetes environment is separate from the Docker Compose deployment, with independent application workloads and database storage. Traefik routes traffic through an Ingress using `taskflow.local`, with TLS configured using a self-signed certificate.

## Technology Stack

| **Area**             | **Technologies**                                              |
| -------------------- | ------------------------------------------------------------- |
| Application          | Python 3.12, FastAPI, Uvicorn                                 |
| Database             | PostgreSQL 16                                                 |
| Database access      | SQLAlchemy 2, psycopg                                         |
| Containers           | Docker, Docker Compose                                        |
| Reverse proxy        | Nginx                                                         |
| CI/CD                | GitHub Actions                                                |
| Container registry   | GitHub Container Registry (GHCR)                              |
| Private connectivity | Tailscale, SSH                                                |
| Kubernetes           | K3s, kubectl, Ingress, Traefik                                |
| Packaging            | Helm                                                          |
| Kubernetes workloads | Deployments, StatefulSets, Pods                               |
| Networking           | ClusterIP Services, Headless Services, NetworkPolicies        |
| Configuration        | ConfigMaps, Kubernetes Secrets                                |
| Storage              | PersistentVolumes, PersistentVolumeClaims, local-path         |
| Scaling              | Horizontal Pod Autoscaler (HPA)                               |
| Container security   | SecurityContext, non-root containers, capability restrictions |
| Monitoring           | Prometheus, Node Exporter                                     |
| Visualization        | Grafana                                                       |
| Alerting             | Alertmanager, Telegram                                        |
| Metrics queries      | PromQL                                                        |

## Repository Structure

```
.
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── docker/
│   └── nginx/
│       └── compose.yaml
├── docs/
│   ├── architecture/
│   │   └── overview.md
│   ├── decisions/
│   ├── incidents/
│   └── learning-log/
│       ├── 2026-11-03.md
│       ├── 2026-11-04.md
│       ├── 2026-11-05.md
│       ├── 2026-11-07.md
│       ├── 2026-11-08.md
│       ├── 2026-11-09.md
│       ├── 2026-11-10.md
│       ├── 2026-11-11.md
│       ├── 2026-11-12.md
│       ├── 2026-11-14.md
│       ├── 2026-11-16.md
│       ├── 2026-11-18.md
│       ├── 2026-11-19.md
│       ├── 2026-11-21.md
│       ├── 2026-11-22.md
│       ├── 2026-11-23.md
│       └── 2026-11-24.md
├── helm/
│   └── taskflow/
│       ├── templates/
│       │   ├── configmap.yaml
│       │   ├── deployment.yaml
│       │   ├── _helpers.tpl
│       │   ├── ingress.yaml
│       │   ├── postgres-headless.yaml
│       │   ├── postgres-service.yaml
│       │   ├── postgres-statefulset.yaml
│       │   ├── serviceaccount.yaml
│       │   └── service.yaml
│       ├── Chart.yaml
│       └── values.yaml
├── k8s/
│   ├── api-service.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── namespace.yaml
│   ├── networkpolicy-api.yaml
│   ├── networkpolicy-postgres.yaml
│   ├── postgres-headless.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-secret.yaml
│   ├── postgres-service.yaml
│   ├── postgres-statefulset.yaml
│   └── serviceaccount.yaml
├── prometheus/
│   ├── rules/
│   │   └── alerts.yml
│   ├── alertmanager.yml
│   └── prometheus.yml
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── secrets/
│   └── telegram_bot_token
├── docker-compose.yml
├── Dockerfile
├── index.html
├── nginx.conf
├── README.md
├── requirements.txt
└── taskflow-backup.sql

```

- `app/` — FastAPI application, database configuration, models, schemas and task routes.
- `docker/` and the root Compose files — Docker Compose setup and Nginx-related configuration.
- `k8s/` — Kubernetes manifests for the K3s deployment.
- `helm/taskflow/` — Helm chart templates and chart values. The chart has been linted and rendered locally; it has not been installed as a Helm release in the live cluster.
- `prometheus/` — Prometheus and Alertmanager configuration, including alert rules.
- `tests/` — application tests used by CI.
- `docs/` — architecture documentation, decision records, incident notes and dated learning logs.
- `secrets/` and `taskflow-backup.sql` — local sensitive material. These must not be committed or exposed publicly; ensure they are excluded by `.gitignore` and rotate any credentials if they were exposed.

## Running the Docker Compose Environment

### Prerequisites

- Docker Engine
- Docker Compose plugin
- Git

### 1. Clone the repository

```
git clone https://github.com/KuroHakke003/taskflow-devops.git
cd taskflow-devops
```

### 2. Configure environment variables

Create `.env` from `.env.example` and adjust values as needed. The Compose deployment uses the database service name `db` as the database hostname. Do not commit `.env`.

### 3. Pull and start services

```
docker compose pull
docker compose up -d
```

### 4. Check status and logs

```
docker compose ps
docker logs api_service
```

## Application Access

In the Docker Compose environment, Nginx is exposed on host port `80`. The API container listens internally on port `8000` and is not directly published to the host in the current configuration.

| **Endpoint**    | **Purpose**               |
| --------------- | ------------------------- |
| `/docs`         | Swagger UI                |
| `/openapi.json` | OpenAPI schema            |
| `/tasks`        | Task management endpoints |
| `/health/live`  | Liveness check            |
| `/health/ready` | Readiness check           |

Private remote access to the Compose deployment is provided through the configured Tailscale Serve HTTPS address.

## CI/CD

The GitHub Actions workflow is located at `.github/workflows/cd.yml` and is named **TaskFlow CI/CD**.

### Pipeline

On pushes and pull requests targeting `main`, the workflow runs tests using Python 3.12 and PostgreSQL 16. For pushes to `main`, successful tests are followed by a Docker image build and publication to GHCR, then an automated deployment to K3s.

```
Push to main
    |
    v
GitHub Actions
    |
    v
Run pytest + PostgreSQL service
    |
    v
Build Docker image
    |
    v
Publish to GHCR (latest + commit SHA)
    |
    v
Connect runner to Tailscale
    |
    v
Restricted SSH to deployment host
    |
    v
Update K3s Deployment image
    |
    v
Wait for rollout status

```

### CI: testing

- Python 3.12 environment.
- PostgreSQL 16 service container with a health check.
- Dependency installation from `requirements.txt`.
- Automated tests using `pytest`.

### Image build and publishing

- Docker image builds after the test job succeeds.
- Images are published to GHCR.
- The workflow publishes both `latest` and the full Git commit SHA as image tags.
- Publishing is restricted to pushes to `main`.

Image repository:

```
ghcr.io/kurohakke003/taskflow-devops

```

### Automated K3s deployment

The deployment job connects to the K3s host through Tailscale, then uses SSH to invoke a restricted deployment command.

- Tailscale connects the GitHub Actions runner to the private tailnet.
- SSH uses a dedicated `taskflow-deploy` account and dedicated key.
- The authorized key is restricted to a forced command through an SSH wrapper.
- The wrapper accepts a deployment command containing a valid commit SHA.
- A restricted sudo rule permits the deployment user to execute the dedicated deployment script.
- The script updates the `taskflow-api` container image in the `taskflow-api` Deployment.
- `kubectl rollout status` waits for rollout completion.

The workflow deploys a commit-specific image tag rather than relying on `latest` for the Kubernetes update.

### Successful deployment verification

The pipeline has been successfully executed end-to-end. The K3s Deployment was updated and the rollout completed successfully. The API Deployment was subsequently verified with two ready replicas, and both replacement API Pods were Running and Ready.

## Data Persistence

### Docker Compose

The Compose PostgreSQL service stores its data in the named Docker volume `postgres_data`.

- `docker compose down` removes containers and the Compose network but preserves named volumes.
- `docker compose down -v` also removes named volumes and their stored database data. Use it only when intentionally deleting that data.

Prometheus uses `prometheus_data` for collected metrics. Grafana stores application data under `/var/lib/grafana`.

### Kubernetes

The Kubernetes PostgreSQL workload uses `postgres-pvc`:

- Storage request: `2Gi`
- Access mode: `ReadWriteOnce`
- Storage class: K3s `local-path`
- Status: `Bound`

The PVC is attached to the PostgreSQL StatefulSet. Persistent storage resources should not be removed during routine troubleshooting unless data deletion is intentional.

## Monitoring and Observability

The monitoring stack consists of Prometheus, Node Exporter, Alertmanager, Grafana and Telegram notifications.

### Prometheus and Node Exporter

Prometheus collects and stores time-series metrics from configured targets. Node Exporter exposes Linux host-level metrics, including CPU, memory, filesystem, network and system information.

### Grafana

Grafana visualizes collected metrics through dashboards, including host CPU, memory, disk usage and resource utilization over time.

### Alertmanager and Telegram

Alertmanager handles alerts and routes notifications to Telegram. A `HighCPUUsage` alert has been configured and tested, including successful notification delivery.

### PromQL

Queries explored include `rate()`, `time()`, `node_boot_time_seconds` and `node_network_receive_bytes_total`.

Example uptime query:

```
time() - node_boot_time_seconds

```

Example network receive rate:

```
rate(node_network_receive_bytes_total[5m])

```

Monitoring and alerting have been implemented and are part of the operational capabilities practiced in this project.

## Kubernetes (K3s)

The K3s environment is deployed in a dedicated `taskflow` namespace.

### Implemented Kubernetes concepts

- K3s cluster initialization and node inspection.
- Traefik Ingress Controller, Ingress routing and TLS.
- Namespaces, Pods, Deployments and Services.
- ConfigMaps and Secrets.
- PersistentVolumes and PersistentVolumeClaims.
- Liveness and readiness probes.
- CPU and memory requests and limits.
- Metrics API and resource inspection using `kubectl top`.
- Horizontal Pod Autoscaler (HPA) and scale-up testing.
- PostgreSQL StatefulSet and headless Service.
- ServiceAccounts and token mount control.
- RBAC and least-privilege principles.
- Container and Pod security hardening.
- NetworkPolicies and network isolation testing.

### TaskFlow API

- Deployment: `taskflow-api`.
- Service: `taskflow-api` (ClusterIP).
- Configuration: `taskflow-config` ConfigMap.
- Database credentials: `postgres-secret` Secret.
- Liveness and readiness probes.
- CPU and memory requests and limits.
- Runs as a non-root user.
- Dedicated ServiceAccount with automatic token mounting disabled.
- HPA scaling based on CPU and memory utilization.
- NetworkPolicy restricts ingress to allowed in-namespace workloads and Traefik.

### PostgreSQL

- StatefulSet: `postgres`.
- PostgreSQL 16.
- Credentials stored in `postgres-secret`.
- PVC: `postgres-pvc`.
- Headless Service: `postgres-headless`.
- Application connectivity through the `db` ClusterIP Service.
- CPU and memory requests and limits.
- NetworkPolicy allows PostgreSQL ingress from TaskFlow API Pods on TCP/5432.

### Configuration

The `taskflow-config` ConfigMap contains non-sensitive application settings such as `APP_NAME`, `APP_ENV`, `APP_HOST` and `APP_PORT`. The `postgres-secret` Secret contains database settings and credentials. Secret values are not committed to the repository.

### Health checks and resources

The API Deployment uses `/health/live` for liveness and `/health/ready` for readiness.

| **Workload** | **Resource** | **Request** | **Limit** |
| ------------ | ------------ | ----------- | --------- |
| TaskFlow API | CPU          | 100m        | 500m      |
| TaskFlow API | Memory       | 128Mi       | 256Mi     |
| PostgreSQL   | CPU          | 100m        | 500m      |
| PostgreSQL   | Memory       | 128Mi       | 512Mi     |

### Horizontal Pod Autoscaler

The API HPA (`api-hpa`) has been configured and tested:

- Minimum replicas: 1
- Maximum replicas: 3
- CPU utilization target: 50% of requested CPU
- Memory utilization target: 70% of requested memory

A load test using a temporary BusyBox Pod successfully triggered scaling from one replica up to the configured maximum of three. PostgreSQL is not scaled by this HPA.

### Security hardening

The API container and Pod use restricted execution settings, including:

- `runAsNonRoot: true`
- Non-root user/group IDs
- `allowPrivilegeEscalation: false`
- Dropped Linux capabilities
- Read-only root filesystem in the hardened Kubernetes configuration
- Dedicated ServiceAccount
- Disabled automatic ServiceAccount token mounting

The API does not currently require Kubernetes API permissions, so no additional permissions are granted to its ServiceAccount.

### NetworkPolicies

Two NetworkPolicies are applied in the `taskflow` namespace.

**PostgreSQL policy:** allows ingress on TCP/5432 only from TaskFlow API Pods in the namespace.

**API policy:** allows ingress on TCP/8000 from permitted namespace workloads and Traefik in `kube-system`; egress is not currently restricted.

Network isolation was tested using temporary Pods and a temporary namespace:

- In-namespace access to the API was verified.
- API access from an external test namespace was blocked.
- Direct Pod-IP access from the external test namespace was blocked.
- PostgreSQL access from an unauthorized test Pod was blocked.

Temporary testing resources were removed after testing.

### Ingress and TLS

- Traefik Ingress Controller.
- Ingress hostname: `taskflow.local`.
- API Service backend: `taskflow-api:8000`.
- Self-signed TLS certificate with a SAN for `taskflow.local`.
- TLS Secret: `taskflow-tls`.
- HTTP and HTTPS access verified, including `/docs`.
- NetworkPolicy troubleshooting to allow Ingress Controller traffic.
- Local hostname resolution configured for testing.

Self-signed certificates are used for this learning environment and are not equivalent to a publicly trusted certificate.

## Helm

A Helm chart is maintained under `helm/taskflow/` to template and package Kubernetes configuration.

### Chart progress

- Initialized chart structure and `Chart.yaml`.
- Created reusable template helpers for chart names, labels and selectors in `_helpers.tpl`.
- Templated the API Deployment and parameterized replicas, image, pull policy, service port, resources and security settings.
- Added Pod and container security settings, including non-root execution, `fsGroup`, privilege escalation restrictions, dropped capabilities and read-only root filesystem.
- Included resource requests/limits, environment references and health probes in chart configuration.
- Aligned Deployment selectors and Pod labels with the existing live Deployment.
- Aligned resource naming and Service selectors with existing Kubernetes resources.
- Aligned Ingress host, TLS Secret and Service backend settings.
- Checked PostgreSQL resource references and persistent storage settings without modifying the live database.

### Validation

```
helm lint helm/taskflow
helm template taskflow helm/taskflow -n taskflow
```

Both validation commands passed. The chart was rendered and inspected locally but has not been installed into or used to adopt the live cluster resources. Helm release installation, upgrades and rollbacks remain future practice.

## Backup and Recovery

An operational PostgreSQL backup and recovery workflow has been implemented and tested against populated TaskFlow data.

### Backup and restore verification

- Created test tasks through the TaskFlow API to ensure the database contained real application data.
- Generated PostgreSQL SQL dumps using `pg_dump` executed inside the Kubernetes PostgreSQL Pod.
- Restored backups into separate test databases (`taskflow_restore_test` and `taskflow_restore_automated_test`) without modifying the original database.
- Verified that all three task records were recovered successfully in both restore tests.

### Backup automation

The backup script is located at `/home/kuro/backup-taskflow.sh` and stores backups under `/home/kuro/backups/taskflow/postgres`.

The script implements:

- Timestamped backup filenames.
- Automatic backup-directory creation.
- Dump generation through `kubectl exec`.
- Temporary-file handling and cleanup with `trap`.
- Validation of the dump file using `test -s`.
- Finalization via `mv` only after validation.
- Failure handling with `set -e`.
- Automatic deletion of backups older than seven days.

### Scheduling

- Configured root Cron to run the backup daily at 02:00.
- Redirected output and errors to `/home/kuro/backups/taskflow/backup.log`.
- Tested scheduling with a temporary every-minute Cron entry.
- Moved execution to root's Cron because the K3s administrative kubeconfig is root-restricted and user Cron could not use interactive sudo.
- Removed `sudo` from the script and used an absolute `kubectl` path.

A failure scenario was tested using an incorrect Pod name. The script exited on failure, removed its temporary file and did not proceed with retention cleanup. An automated backup was subsequently restored and verified with all three task records.


## Operations and Troubleshooting

Practical experience gained includes:

- Inspecting container resource usage with `docker stats`.
- Reviewing and filtering API, PostgreSQL and Nginx logs.
- Investigating database connectivity failures and Docker DNS.
- Reproducing database outages and observing application behavior.
- Inspecting Linux processes using `htop`, `ps` and process information.
- Investigating container runtime processes and `containerd-shim-runc-v2`.
- Troubleshooting Kubernetes Pods, Services, deployments and container startup failures.
- Inspecting Kubernetes resources using `kubectl top`.
- Monitoring HPA scaling behavior.
- Working with PostgreSQL StatefulSets and persistent storage.
- Creating, automating, scheduling and inspecting PostgreSQL backups; restoring populated backups and verifying recovered records.
- Investigating Deployment rollouts, ReplicaSets, rollout revisions and failed image updates.
- Recovering deployments using both standard and revision-specific rollbacks.
- Troubleshooting readiness probe failures using Pod conditions, events and `kubectl describe`.
- Investigating HPA scaling decisions, metrics, requests, limits and stabilization behavior.
- Testing Kubernetes network isolation.
- Troubleshooting GitHub Actions, SSH, Tailscale and automated deployments.

### Kubernetes Rollout, Rollback, Readiness and HPA Practice — November 24, 2026

- Triggered a Deployment rollout through a Pod-template annotation change and observed the new ReplicaSet and revision.
- Simulated an image update failure using a nonexistent image tag and inspected the resulting `ImagePullBackOff` state.
- Verified that existing healthy replicas remained available during the failed rollout.
- Recovered using `kubectl rollout undo` and also practiced a targeted rollback to a selected revision.
- Deliberately misconfigured the readiness probe endpoint, observed a Running but NotReady Pod and investigated the HTTP 404 probe events.
- Verified that readiness failure did not cause container restarts and that the liveness probe remained unaffected.
- Repaired the readiness endpoint and confirmed a successful rollout with healthy, Ready replicas.
- Investigated HPA replica changes, metrics, resource requests and scale-down stabilization; confirmed the API replicas remained healthy.

### Incident: High CPU Usage — November 16, 2026

The Grafana dashboard reported CPU utilization of approximately 99.9%, and Alertmanager successfully delivered a `HighCPUUsage` notification to Telegram.

Stopping K3s did not immediately resolve the CPU overload. Investigation using `htop` revealed four runaway `gosu postgres` processes, each consuming approximately 200% CPU. Their shared parent process was identified as `containerd-shim-runc-v2`. The processes continued running after the K3s service had been stopped.

After terminating the processes, CPU utilization dropped significantly:

| **Metric**           | **Before** | **After** |
| -------------------- | ---------- | --------- |
| CPU 0                | 100%       | 2.8%      |
| CPU 1                | 100%       | 0.8%      |
| Load average (1 min) | 5.04       | 3.87      |
| RAM                  | 927 MB     | 893 MB    |

The processes were identified as the immediate cause of the overload. The underlying reason they became stuck remains under investigation.

### Incident: Prometheus Instrumentator Compatibility — November 18, 2026

The TaskFlow API returned HTTP 500 errors due to a compatibility issue with `prometheus-fastapi-instrumentator` 7.1.0. The middleware failed with an `AttributeError` involving an internal FastAPI router object.

The dependency constraint in `requirements.txt` was adjusted to avoid the incompatible version. After rebuilding and deploying the updated image, API endpoints were verified again.

### CI/CD Deployment Troubleshooting — November 23, 2026

During implementation of the automated deployment pipeline, several issues were identified and corrected:

- SSH was listening on port 2222 rather than the default port 22; the workflow SSH commands were updated.
- The deployment script referenced the wrong `kubectl` path; it was corrected to `/usr/local/bin/kubectl`, the K3s symlink.
- The deployment script initially used the wrong container name; it was corrected to `taskflow-api`.
- The deployment pipeline was rerun and completed successfully.

The troubleshooting process helped validate the runner's private network connection, restricted SSH execution, deployment script and Kubernetes rollout verification.

## Project Roadmap

### Completed

- [x] Linux fundamentals and networking
- [x] Git and GitHub workflow
- [x] Docker and Docker Compose
- [x] Nginx reverse proxy
- [x] CI tests with GitHub Actions
- [x] Docker image build and GHCR publishing
- [x] Private remote access through Tailscale
- [x] Monitoring with Prometheus and Node Exporter
- [x] Grafana dashboards
- [x] Alertmanager and Telegram notifications
- [x] K3s cluster setup
- [x] Kubernetes Namespaces, Deployments, Pods and Services
- [x] ConfigMaps and Secrets
- [x] Persistent storage with PVCs
- [x] Liveness and readiness probes
- [x] CPU and memory requests and limits
- [x] Kubernetes resource monitoring
- [x] HPA configuration and scale-up testing
- [x] PostgreSQL migration to StatefulSet
- [x] PostgreSQL backup and restore testing, including populated data, automation, Cron scheduling and retention
- [x] Dockerfile and Kubernetes container security hardening
- [x] Dedicated ServiceAccount and disabled automatic token mounting
- [x] RBAC and least-privilege approach
- [x] PostgreSQL and API NetworkPolicies
- [x] Network isolation testing
- [x] Traefik Ingress and external routing
- [x] TLS configuration and HTTPS testing
- [x] Helm chart templating, linting and rendering validation
- [x] Automated Kubernetes CI/CD deployment through GitHub Actions, GHCR, Tailscale and restricted SSH
- [x] Kubernetes troubleshooting, rolling updates, failed rollout recovery, targeted rollback, readiness probe troubleshooting and HPA investigation

### Planned

- [ ] Helm release installation, upgrades and rollbacks
- [ ] Terraform and Infrastructure as Code
- [ ] AWS fundamentals and cloud infrastructure
- [ ] Terraform-managed AWS infrastructure
- [ ] EKS deployment and cloud-based TaskFlow portfolio environment

---

TaskFlow is a learning and portfolio environment. It demonstrates practical DevOps implementation and troubleshooting, but it is not intended to be represented as a production-ready system.
