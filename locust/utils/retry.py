from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int
    delay: float


DEFAULT_RETRY = RetryPolicy(
    attempts=1,
    delay=0.0,
)


def should_retry(
    status_code: int,
) -> bool:

    return status_code >= 500


def get_retry_policy():

    return DEFAULT_RETRY
