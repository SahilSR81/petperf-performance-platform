from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from locust.assertions.thresholds import PERFORMANCE_THRESHOLDS

logger = logging.getLogger(__name__)


@dataclass
class AssertionResult:
    metric: str
    threshold: float
    actual: float
    passed: bool

    @property
    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"[{status}] {self.metric}: {self.actual:.2f} (threshold: {self.threshold})"
        )


@dataclass
class SLAResult:
    results: list[AssertionResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def overall_status(self) -> str:
        return "PASS" if self.passed else "FAIL"

    def log_summary(self) -> None:
        for result in self.results:
            if result.passed:
                logger.info(result.summary)
            else:
                logger.error(result.summary)
        logger.info("Overall SLA Status: %s", self.overall_status)


def validate_response_time(
    avg_response_time: float,
    threshold: float | None = None,
) -> AssertionResult:
    max_rt = threshold or PERFORMANCE_THRESHOLDS["response_time"]
    passed = avg_response_time <= max_rt
    result = AssertionResult(
        metric="Response Time (ms)",
        threshold=max_rt,
        actual=avg_response_time,
        passed=passed,
    )
    return result


def validate_failure_rate(
    failure_rate: float,
    threshold: float | None = None,
) -> AssertionResult:
    max_fr = threshold or PERFORMANCE_THRESHOLDS["failure_rate"]
    passed = failure_rate <= max_fr
    result = AssertionResult(
        metric="Failure Rate (%)",
        threshold=max_fr,
        actual=failure_rate,
        passed=passed,
    )
    return result


def validate_rps(
    requests_per_second: float,
    threshold: float | None = None,
) -> AssertionResult:
    min_rps = threshold or PERFORMANCE_THRESHOLDS["requests_per_second"]
    passed = requests_per_second >= min_rps
    result = AssertionResult(
        metric="Requests per Second",
        threshold=min_rps,
        actual=requests_per_second,
        passed=passed,
    )
    return result


def validate_all(
    stats: dict[str, Any],
    overrides: dict[str, float] | None = None,
) -> SLAResult:
    overrides = overrides or {}

    avg_response_time = stats.get("avg_response_time", 0)
    failure_rate = stats.get("failure_rate", 0)
    rps = stats.get("requests_per_second", 0)

    rt_threshold = overrides.get("response_time")
    fr_threshold = overrides.get("failure_rate")
    rps_threshold = overrides.get("requests_per_second")

    results = [
        validate_response_time(avg_response_time, rt_threshold),
        validate_failure_rate(failure_rate, fr_threshold),
        validate_rps(rps, rps_threshold),
    ]

    sla_result = SLAResult(results=results)
    sla_result.log_summary()
    return sla_result
