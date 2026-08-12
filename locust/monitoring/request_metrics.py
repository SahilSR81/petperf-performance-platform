from dataclasses import dataclass

from .prometheus_exporter import record_request


@dataclass
class RequestMetric:
    method: str
    name: str
    response_time: float
    response_size: int
    success: bool


class RequestMetricsCollector:

    def __init__(self):
        self.metrics: list[RequestMetric] = []

    def record(
        self,
        method: str,
        name: str,
        response_time: float,
        response_size: int,
        success: bool,
    ):
        self.metrics.append(
            RequestMetric(
                method=method,
                name=name,
                response_time=response_time,
                response_size=response_size,
                success=success,
            )
        )
        record_request(
            method=method,
            name=name,
            response_time=response_time,
            success=success,
        )

    @property
    def total_requests(self) -> int:
        return len(self.metrics)

    @property
    def failed_requests(self) -> int:
        return sum(
            not metric.success
            for metric in self.metrics
        )
