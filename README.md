<div align="center">

# PetPerf

### Production-Grade Performance Engineering Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Locust](https://img.shields.io/badge/Locust-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
[![Performance Tests](https://github.com/SahilSR81/petperf-performance-platform/actions/workflows/perf.yml/badge.svg)](https://github.com/SahilSR81/petperf-performance-platform/actions/workflows/perf.yml)
![Status](https://img.shields.io/badge/Status-Development-orange)

---

> PetPerf simulates real-world traffic, measures how a system behaves under load, and feeds the results into automated tests and dashboards.

</div>

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
locust -f locust/locustfile.py
```

Headless:

```bash
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --host https://petstore3.swagger.io
```

Docker:

```bash
docker compose up
```

---

## Capabilities

- Modular task architecture with read/write separation
- Environment-driven configuration
- Response validation (status code, content-type)
- Workload profiles: smoke, load, stress, spike, soak
- Load shapes: step, ramp-up, spike, endurance
- SLA validation with configurable thresholds
- Prometheus metrics + Grafana dashboards + Pushgateway
- HTML and CSV reporting
- Structured logging with execution telemetry
- Retry policy abstraction
- GitHub Actions CI pipeline with artifact uploads

---

## Layout

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

Structured logs with UTC timestamps; optional file logging via `LOG_FILE`. Metrics use standardized request names so dashboards and reports stay consistent.

On `test_stop` the run prints an execution summary (target environment, user configuration, timestamp) and classifies each response by status-code family: 5xx as server errors, 4xx as client errors.

---

## Observability

Prometheus scrapes the Locust process via `/metrics` on port `9091`. Metrics include latency histograms, active users, in-flight requests, and error counters, labeled by method, endpoint, and status.

Grafana dashboards are auto-provisioned with panels for response time (p50/p95/p99), error rate, active users, and throughput.

For ephemeral runs, set `PUSHGATEWAY_URL` to push metrics instead:

```bash
docker compose -f docker-compose.observability.yml up
```

---

## SLA Validation

Thresholds live in `locust/assertions/thresholds.py`:

```python
PERFORMANCE_THRESHOLDS = {
    "response_time": 1000,
    "failure_rate": 1.0,
    "requests_per_second": 20,
}
```

Validation runs on `test_stop` and logs a per-metric PASS/FAIL summary plus an overall status:

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

HTML reports cover response time, throughput, error rate, execution metadata, and SLA result. Saved to `reports/latest-report.html`.

Pass `--csv <prefix>` for per-second CSV output (`_stats.csv`, `_stats_history.csv`, `_failures.csv`, `_exceptions.csv`).

---

## Distributed Mode

Master coordinates, workers execute, stats aggregate at the master:

```bash
locust -f locust/locustfile.py --master --headless -u 100 -r 10 -t 30m
locust -f locust/locustfile.py --worker --master-host=localhost
```

---

## API Client Layer

All HTTP goes through `locust/utils/api_client.py`. Every request carries an `X-Correlation-ID` (UUID) and `User-Agent` from `locust/utils/request_context.py` and is checked against the retry policy in `locust/utils/retry.py` (no-op by default; automatic retries are a future milestone). Responses are classified by status-code family in one place, so workloads never reimplement that logic.

---

## CI Gate

The GitHub Actions workflow (`.github/workflows/perf.yml`) runs headless Locust on schedule (weekdays 06:00 UTC) or via `workflow_dispatch`, then uploads CSV and HTML artifacts. SLA validation runs inside the test and logs PASS/FAIL on `test_stop`. The pipeline always exits 0; results live in the logs and the HTML report.

```bash
gh workflow run perf.yml -f users=50 -f spawn_rate=10 -f run_time=10m
```

---

## Recommended Runs

```bash
# Smoke
locust -f locust/locustfile.py --headless -u 5 -r 2 -t 2m

# Load
locust -f locust/locustfile.py --headless -u 50 -r 10 -t 15m --csv reports/load-test

# Stress
locust -f locust/locustfile.py --headless -u 200 -r 50 -t 5m --csv reports/stress-test

# Soak
locust -f locust/locustfile.py --headless -u 30 -r 5 -t 60m --csv reports/soak-test

# Spike
locust -f locust/locustfile.py --headless --shape-class SpikeShape --csv reports/spike-test

# CI run
locust -f locust/locustfile.py --headless -u 25 -r 5 -t 5m --csv reports/ci-run
```

---

## Roadmap

### Phase 1: Foundation
- [x] Repository initialization
- [x] Development environment bootstrap
- [x] Modular task architecture
- [x] Configuration layer
- [x] Response validation
- [x] Docker runtime

### Phase 2: Observability
- [x] Prometheus metrics
- [x] Grafana dashboards
- [x] CSV reporting
- [x] SLA validation

### Phase 3: Automation
- [x] GitHub Actions CI pipeline
- [x] Stress / spike / soak testing
- [x] Distributed load testing

### Phase 4: Resilience
- [ ] Retry strategy

---

<div align="center">

**Building in public.**

</div>
