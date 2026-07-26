from prometheus_client import Counter, Gauge, Histogram

REQUEST_LATENCY = Histogram(
    "petperf_request_latency_seconds",
    "Request latency distribution",
    labelnames=["method", "endpoint", "status"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

ACTIVE_USERS = Gauge(
    "petperf_active_users",
    "Number of active virtual users",
)

INFLIGHT_REQUESTS = Gauge(
    "petperf_inflight_requests",
    "Number of requests currently in flight",
)

ERRORS_TOTAL = Counter(
    "petperf_errors_total",
    "Total number of failed requests",
    labelnames=["method", "endpoint", "error_type"],
)

REQUESTS_TOTAL = Counter(
    "petperf_requests_total",
    "Total number of requests",
    labelnames=["method", "endpoint", "status"],
)
