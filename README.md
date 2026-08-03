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
- Predefined workload profiles (smoke, load, stress, spike, soak)
- Load shape patterns (step, ramp-up, spike, endurance)
- Read and write task separation
- GitHub Actions CI pipeline with artifact uploads
- SLA validation with configurable thresholds
- Automated HTML reporting

---

## Folder Structure

```text
petperf-performance-platform/
│
├── .github/
│   └── workflows/
│       └── perf.yml
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
│   ├── load_shapes.py
│   ├── assertions/
│   │   ├── __init__.py
│   │   ├── sla.py
│   │   └── thresholds.py
│   ├── data/
│   │   ├── pets.json
│   │   ├── pet_status.json
│   │   └── users.json
│   ├── reports/
│   │   ├── __init__.py
│   │   └── html_report.py
│   ├── scenarios/
│   │   ├── __init__.py
│   │   ├── smoke.py
│   │   ├── load.py
│   │   ├── stress.py
│   │   ├── spike.py
│   │   └── soak.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── pet_read_tasks.py
│   │   └── pet_write_tasks.py
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── execution_profile.py
│       ├── payload_factory.py
│       ├── settings.py
│       ├── validators.py
│       ├── logging_config.py
│       └── run_context.py
│
├── reports/
│   └── .gitkeep
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

## Workload Profiles

Predefined workload profiles are available in `locust/scenarios/`:

| Profile | File | Purpose | Users | Wait Time |
|---------|------|---------|-------|-----------|
| **Smoke** | `smoke.py` | Quick validation | Minimal | 1–2s |
| **Load** | `load.py` | Normal expected traffic | Moderate | 0.5–2s |
| **Stress** | `stress.py` | Push system limits | High | 0.1–0.5s |
| **Spike** | `spike.py` | Sudden burst behavior | Burst | 0.3–1s |
| **Soak** | `soak.py` | Long-duration endurance | Sustained | 2–5s |

Each profile defines user behaviour with appropriate read/write ratios and think times.

---

## Data-Driven Workloads

Performance scenarios are powered by reusable datasets instead of hardcoded values.

Current datasets include:

- Pet records
- Status combinations
- User execution profiles

Benefits:

- Improved maintainability
- Reusable workloads
- Better scalability
- Easier test expansion

---

## Framework Design

The framework separates responsibilities into independent layers.

- Configuration Layer
- Scenario Layer
- Task Layer
- Data Layer
- Reporting Layer
- Monitoring Layer

This architecture allows new workloads to be introduced with minimal changes to existing code.

### Execution Profiles

Execution parameters are centrally managed through reusable execution profiles.

This keeps load configurations consistent across local and CI executions.

```text
locust/
├── tasks/
├── utils/
├── assertions/
├── reports/
├── scenarios/
├── data/
└── locustfile.py
```

---

## Load Shapes

Custom load shapes in `locust/load_shapes.py` control how users are spawned over time:

| Shape | Pattern |
|-------|---------|
| `StepLoadShape` | Increment users in steps every 60s |
| `RampUpShape` | Linear ramp-up to target count |
| `SpikeShape` | Baseline → spike → recovery cycles |
| `EnduranceShape` | Ramp-up then hold for extended period |

Use a shape with `--shape-class`:

```bash
locust -f locust/locustfile.py --headless --shape-class StepLoadShape -t 10m
```

---

## Performance Validation

The framework evaluates every execution against configurable Service Level thresholds.

Current validation includes:

- Maximum response time
- Failure percentage
- Requests per second
- Overall execution status (PASS / FAIL)

Thresholds are defined in `locust/assertions/thresholds.py` and can be updated without modifying validation logic:

```python
PERFORMANCE_THRESHOLDS = {
    "response_time": 1000,
    "failure_rate": 1.0,
    "requests_per_second": 20,
}
```

Usage:

```python
from locust.assertions import validate_all

result = validate_all(stats={
    "avg_response_time": 450,
    "failure_rate": 0.5,
    "requests_per_second": 35,
})

print(result.overall_status)  # PASS or FAIL
```

---

## Reporting

Following every execution the framework can generate an HTML summary including:

- Response Time
- Throughput
- Error Rate
- Execution Metadata
- SLA Result

Generated reports are saved to `reports/latest-report.html`.

```python
from locust.reports import generate_html_report

report_path = generate_html_report(
    stats=stats,
    run_metadata=run_metadata,
    sla_status=sla_result.overall_status,
)
```

---

### Request Naming

Performance metrics use standardized request names to improve report readability and maintain consistency across dashboards and execution reports.

---

### Execution Metadata

Every execution records basic framework information including framework version, Python runtime, execution timestamp and target environment.

This metadata helps correlate performance reports with specific framework versions and environments.

---

### API Client Layer

HTTP communication is routed through a lightweight client wrapper.

This abstraction keeps request behavior centralized and allows future enhancements such as retries, authentication, logging and custom headers without modifying individual workload definitions.

---

## Headless Execution

Locust supports headless (non-UI) mode for automation and CI:

```bash
locust -f locust/locustfile.py --headless -u 50 -r 5 -t 10m --host https://petstore3.swagger.io
```

For distributed runs:

```bash
# Start master
locust -f locust/locustfile.py --master --headless -u 100 -r 10 -t 30m

# Start workers
locust -f locust/locustfile.py --worker --master-host=localhost
```

---

## CSV Reports

Pass `--csv <prefix>` to generate CSV output with per-second granularity:

```bash
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --csv reports/run --exit-code-on-error
```

Generated files:
- `<prefix>_stats.csv` — aggregated statistics
- `<prefix>_stats_history.csv` — time-series stats
- `<prefix>_failures.csv` — failure breakdown
- `<prefix>_exceptions.csv` — exception log

---

## CI Gate

The GitHub Actions workflow (`.github/workflows/perf.yml`) runs headless Locust and fails on non-zero exit:

- Triggered by schedule (weekdays 06:00 UTC) or `workflow_dispatch`
- Installs dependencies, runs the test, uploads CSV and HTML artifacts
- `--exit-code-on-error` ensures the pipeline fails if any request errors occur

```bash
# Manual trigger example
gh workflow run perf.yml -f users=50 -f spawn_rate=10 -f run_time=10m
```

---

## Distributed Testing Ready

The framework supports Locust's native distributed mode:

- **Master** coordinates the test
- **Workers** execute tasks independently
- Connect via `--master` / `--worker` flags
- Stats aggregated at the master node
- Works with all load shapes and scenarios

---

## Recommended Run Examples

```bash
# Smoke test (quick validation)
locust -f locust/locustfile.py --headless -u 5 -r 2 -t 2m --exit-code-on-error

# Load test (normal traffic)
locust -f locust/locustfile.py --headless -u 50 -r 10 -t 15m --csv reports/load-test

# Stress test (push limits)
locust -f locust/locustfile.py --headless -u 200 -r 50 -t 5m --csv reports/stress-test

# Soak test (long duration)
locust -f locust/locustfile.py --headless -u 30 -r 5 -t 60m --csv reports/soak-test

# Spike test with custom shape
locust -f locust/locustfile.py --headless --shape-class SpikeShape --csv reports/spike-test

# CI run
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --csv reports/ci-run --exit-code-on-error
```

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
- [x] CSV reporting
- [x] SLA validation

### Phase 3 — Automation

- [x] GitHub Actions CI pipeline
- [x] Stress testing
- [x] Spike testing
- [x] Soak testing
- [x] Distributed load testing

---

<div align="center">

**Building in public.**

</div>
