<div align="center">

# PetPerf

### Production-Grade Performance Engineering Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Locust](https://img.shields.io/badge/Locust-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
[![Performance Tests](https://github.com/SahilSR81/petperf-performance-platform/actions/workflows/perf.yml/badge.svg)](https://github.com/SahilSR81/petperf-performance-platform/actions/workflows/perf.yml)
![Status](https://img.shields.io/badge/Status-Development-orange)

---

> **PetPerf is a production-oriented Performance Engineering framework built to simulate real-world traffic, analyze system behavior under load, and provide actionable insights through automated testing and observability.**

</div>

---

## Project Philosophy

A production-oriented performance engineering framework rather than a collection of isolated load scripts.

- **Modular architecture** — Tasks, utilities, and configuration are cleanly separated
- **Configuration-driven execution** — Environment variables control targets, load profiles, and runtime behavior
- **Reusable workloads** — Composable task modules, not monolithic scripts
- **Containerized runtime** — Docker for identical execution everywhere
- **CI/CD readiness** — Built for automated pipelines from day one
- **Observability-first** — Metrics, dashboards, and SLA validation are core objectives

---

## Current Capabilities

- Modular task architecture with read/write separation
- Environment-driven configuration
- Response validation (status code, content-type)
- Structured logging with execution telemetry and lifecycle hooks
- Prometheus metrics export + Grafana dashboards + Pushgateway support
- Predefined workload profiles (smoke, load, stress, spike, soak)
- Load shape patterns (step, ramp-up, spike, endurance)
- SLA validation with configurable thresholds
- Automated HTML reporting
- Retry policy abstraction
- GitHub Actions CI pipeline with artifact uploads

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
locust -f locust/locustfile.py
```

Headless mode:

```bash
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --host https://petstore3.swagger.io
```

Docker:

```bash
docker compose up
```

---

## Folder Structure

```text
locust/
├── locustfile.py        # Entry point
├── config.py            # Runtime configuration
├── hooks.py             # Lifecycle hooks
├── load_shapes.py       # Load shape patterns
├── assertions/          # SLA validation
├── data/                # Reusable datasets
├── reports/             # HTML reporting
├── scenarios/           # Workload profiles
├── tasks/               # Read/write task definitions
└── utils/               # retry, api_client, validators, etc.
```

---

## Execution Telemetry

| Event | Trigger | Data Captured |
|-------|---------|---------------|
| `test_start` | Run begins | run_id, target_host, user_count, spawn_rate, run_time, environment |
| `test_stop` | Run ends | duration, total_requests, total_failures, avg_response_time, fail_ratio, sla_status |
| `request` | Per request | method, endpoint, response_time_ms, response_length, error (if failed) |

Structured logging with UTC timestamps; optional file logging via `LOG_FILE`.

---

## Observability Stack

Prometheus scrapes the Locust process via `/metrics` (port `9091`). Metrics include latency histograms, active users, in-flight requests, error counters, and request counters — labeled by method, endpoint, and status.

Grafana dashboards are auto-provisioned with panels for response time (p50/p95/p99), error rate, active users, and throughput.

For ephemeral runs, set `PUSHGATEWAY_URL` to push metrics instead.

```bash
docker compose -f docker-compose.observability.yml up
```

---

## SLA Validation

Every execution is evaluated against configurable thresholds in `locust/assertions/thresholds.py`:

```python
PERFORMANCE_THRESHOLDS = {
    "response_time": 1000,
    "failure_rate": 1.0,
    "requests_per_second": 20,
}
```

Validation runs on `test_stop` and logs a per-metric PASS/FAIL summary plus overall status.

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

HTML summary reports include response time, throughput, error rate, execution metadata, and SLA result. Saved to `reports/latest-report.html`.

Pass `--csv <prefix>` for per-second CSV granularity (`_stats.csv`, `_stats_history.csv`, `_failures.csv`, `_exceptions.csv`).

---

## Workload Profiles & Load Shapes

Predefined profiles in `locust/scenarios/`: **Smoke**, **Load**, **Stress**, **Spike**, **Soak**.

Custom shapes in `locust/load_shapes.py`: `StepLoadShape`, `RampUpShape`, `SpikeShape`, `EnduranceShape`.

```bash
locust -f locust/locustfile.py --headless --shape-class SpikeShape --csv reports/spike-test
```

---

## Request Naming & Execution Metadata

Metrics use standardized request names for consistent dashboards and reports.

Every execution records framework version, Python runtime, execution timestamp, and target environment.

---

## API Client Layer

HTTP communication is routed through a lightweight client wrapper (`locust/utils/api_client.py`), keeping request behavior centralized and workload definitions independent of infrastructure concerns.

### Request Context

Every outgoing request is prepared through a centralized request context.

The framework currently injects a unique correlation identifier and common request headers to improve traceability and prepare the framework for future observability integrations.

### Retry Strategy

The framework introduces a reusable retry policy abstraction.

Current implementation defines retry behavior centrally while keeping workload definitions independent from retry configuration.

Automatic retries will be introduced in a future milestone.

---

## CI Gate

The GitHub Actions workflow (`.github/workflows/perf.yml`) runs headless Locust:

- Triggered by schedule (weekdays 06:00 UTC) or `workflow_dispatch`
- Installs dependencies, runs the test, uploads CSV and HTML artifacts
- SLA validation runs inside the test and logs a PASS / FAIL summary on `test_stop`
- The pipeline always exits 0 — SLA results are captured in logs and the HTML report

```bash
gh workflow run perf.yml -f users=50 -f spawn_rate=10 -f run_time=10m
```

---

## Distributed Testing

Locust's native distributed mode is supported: master coordinates, workers execute, stats aggregate at the master.

```bash
locust -f locust/locustfile.py --master --headless -u 100 -r 10 -t 30m
locust -f locust/locustfile.py --worker --master-host=localhost
```

---

## Recommended Runs

```bash
# Smoke test
locust -f locust/locustfile.py --headless -u 5 -r 2 -t 2m

# Load test
locust -f locust/locustfile.py --headless -u 50 -r 10 -t 15m --csv reports/load-test

# Stress test
locust -f locust/locustfile.py --headless -u 200 -r 50 -t 5m --csv reports/stress-test

# Soak test
locust -f locust/locustfile.py --headless -u 30 -r 5 -t 60m --csv reports/soak-test

# Spike test
locust -f locust/locustfile.py --headless --shape-class SpikeShape --csv reports/spike-test

# CI run
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --csv reports/ci-run
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
- [x] Stress / spike / soak testing
- [x] Distributed load testing

### Phase 4 — Resilience

- [ ] Retry strategy

---

<div align="center">

**Building in public.**

</div>
