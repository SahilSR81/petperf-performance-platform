<div align="center">

# PetPerf

### Production-Grade Performance Engineering Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Locust](https://img.shields.io/badge/Locust-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Status](https://img.shields.io/badge/Status-Development-orange)

---

> **PetPerf is a production-oriented Performance Engineering framework built to simulate real-world traffic, analyze system behavior under load, and provide actionable insights through automated testing and observability.**

</div>

---

## Project Philosophy

This repository is designed as a production-oriented Performance Engineering framework rather than a collection of isolated load scripts.

Key principles:

- **Modular architecture** — Task definitions, utilities, and configuration are cleanly separated.
- **Configuration-driven execution** — Environment variables control targets, load profiles, and runtime behavior.
- **Reusable workloads** — Scenarios are built as composable task modules, not monolithic scripts.
- **Containerized runtime** — Docker ensures identical execution across every machine and CI server.
- **CI/CD readiness** — Designed for integration into automated pipelines from day one.
- **Observability-first design** — Metrics, dashboards, and SLA validation are core objectives, not afterthoughts.

---

## Current Capabilities

- Modular task architecture
- Environment-driven configuration
- Reusable validation utilities
- Executable HTTP workloads
- Response validation (status code, content-type)
- Dockerized execution
- Single-command onboarding
- Structured logging with consistent timestamp format
- Execution telemetry and lifecycle hooks
- Run metadata capture (run_id, target host, user count, spawn rate, duration)
- Prometheus metrics export (latency, active users, errors, throughput)
- Grafana dashboard provisioning
- Pushgateway support for ephemeral runs

---

## Folder Structure

```text
petperf-performance-platform/
│
├── docker/
│   └── Dockerfile
│
├── docker-compose.yml
│
├── monitoring/
│   ├── __init__.py
│   ├── metrics.py
│   └── exporter.py
│
├── prometheus/
│   └── prometheus.yml
│
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── datasource.yml
│   │   └── dashboards/
│   │       └── dashboards.yml
│   └── dashboards/
│       └── petperf-overview.json
│
├── locust/
│   ├── __init__.py
│   ├── locustfile.py
│   ├── config.py
│   ├── hooks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── validators.py
│   │   ├── logging_config.py
│   │   └── run_context.py
│   └── tasks/
│       ├── __init__.py
│       └── pet_tasks.py
│
├── README.md
├── requirements.txt
├── .editorconfig
├── .env.example
└── .gitignore
```

---

## Docker Support

The framework can be executed inside a Docker container, ensuring a consistent runtime across development machines and CI pipelines.

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

### Stop

```bash
docker compose down
```

Once running, the Locust web UI is available at `http://localhost:8089`.

---

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
locust -f locust/locustfile.py
```

---

## Execution Telemetry

The framework captures structured telemetry at every stage of a load test run:

| Event | Trigger | Data Captured |
|-------|---------|---------------|
| `test_start` | Run begins | run_id, target_host, user_count, spawn_rate, run_time, environment |
| `test_stop` | Run ends | duration, total_requests, total_failures, avg_response_time, fail_ratio |
| `request` | Per request | method, endpoint, response_time_ms, response_length, error (if failed) |

---

## Logging Strategy

- **Console logging** — Real-time output to stdout during runs
- **Structured format** — `%(asctime)s | %(levelname)-8s | %(name)s | %(message)s`
- **UTC timestamps** in ISO 8601 format
- **Module-based logger names** for granular control
- Optional file logging via `LOG_FILE` environment variable

---

## Run Metadata

Each test run is assigned a unique `run_id` (timestamp-based) and tracks:

- Target host
- Virtual user count and spawn rate
- Run duration
- Environment name (standalone / master / worker)

Metadata is logged at `test_start` and summarized at `test_stop`.

---

## Lifecycle Hooks

Lifecycle hooks are wired through `locust/hooks.py` using Locust's built-in event system:

- `test_start` — log initialization metadata
- `test_stop` — log summary statistics
- `request` — structured request timing capture, failure tagging

---

## Observability Stack

### Prometheus

Prometheus scrapes metrics from the Locust process via an HTTP endpoint (`/metrics` on port `9091` by default).

**Metrics captured:**

| Metric | Type | Labels |
|--------|------|--------|
| `petperf_request_latency_seconds` | Histogram | method, endpoint, status |
| `petperf_active_users` | Gauge | — |
| `petperf_inflight_requests` | Gauge | — |
| `petperf_errors_total` | Counter | method, endpoint, error_type |
| `petperf_requests_total` | Counter | method, endpoint, status |

**Scrape config** is defined in `prometheus/prometheus.yml`.

### Grafana

Dashboards are auto-provisioned on startup via configuration files in `grafana/provisioning/`.

- **Data source** — `grafana/provisioning/datasources/datasource.yml` connects Grafana to Prometheus
- **Dashboard provisioning** — `grafana/provisioning/dashboards/dashboards.yml` loads JSON models
- **Overview dashboard** — `grafana/dashboards/petperf-overview.json` includes:
  - Response time panels (p50, p95, p99)
  - Error rate panel
  - Active users panel
  - Throughput panel

### Running the stack

```bash
# Start Prometheus and Grafana alongside Locust
docker compose -f docker-compose.observability.yml up
```

For ephemeral/batch runs, set `PUSHGATEWAY_URL` to push metrics instead of exposing an HTTP endpoint.

---

## Roadmap

### Phase 1 — Foundation

- [x] Repository initialization
- [x] Development environment bootstrap
- [x] Modular task architecture
- [x] Configuration layer
- [x] Response validation
- [x] Docker runtime

### Phase 2 — Observability

- [x] Prometheus metrics
- [x] Grafana dashboards
- [ ] SLA validation
- [ ] CSV reporting

### Phase 3 — Automation

- [ ] GitHub Actions CI pipeline
- [ ] Stress testing
- [ ] Spike testing
- [ ] Soak testing
- [ ] Distributed load testing

---

<div align="center">

**Building in public.**

</div>
