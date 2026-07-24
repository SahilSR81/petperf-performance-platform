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
├── locust/
│   ├── __init__.py
│   ├── locustfile.py
│   ├── config.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── validators.py
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

## Roadmap

### Phase 1 — Foundation

- [x] Repository initialization
- [x] Development environment bootstrap
- [x] Modular task architecture
- [x] Configuration layer
- [x] Response validation
- [x] Docker runtime

### Phase 2 — Observability

- [ ] Prometheus metrics
- [ ] Grafana dashboards
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
