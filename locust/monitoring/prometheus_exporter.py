from prometheus_client import Counter, Gauge, Histogram, start_http_server


REQUESTS = Counter(
    "petperf_requests_total",
    "Total number of requests",
    ["method", "name"],
)

FAILURES = Counter(
    "petperf_failures_total",
    "Total number of failed requests",
    ["method", "name"],
)

RESPONSE_TIME = Histogram(
    "petperf_response_time_ms",
    "Request response time in milliseconds",
    ["method", "name"],
)

ACTIVE_USERS = Gauge(
    "petperf_active_users",
    "Current number of active users",
)


def start_metrics_server(port: int = 8000):
    start_http_server(port)


def record_request(
    method: str,
    name: str,
    response_time: float,
    success: bool,
):
    REQUESTS.labels(method, name).inc()
    RESPONSE_TIME.labels(method, name).observe(response_time)

    if not success:
        FAILURES.labels(method, name).inc()


def update_active_users(count: int):
    ACTIVE_USERS.set(count)
