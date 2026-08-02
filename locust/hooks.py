from datetime import datetime, timezone

from locust import events
from locust.runners import MasterRunner, WorkerRunner

from utils.execution_metadata import get_execution_metadata
from utils.logging_config import get_logger
from utils.run_context import RunContext

logger = get_logger(__name__)
run_context = RunContext()


@events.init.add_listener
def on_init(environment, **kwargs):
    run_context.run_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    run_context.target_host = environment.host or ""
    run_context.environment_name = (
        "master"
        if isinstance(environment.runner, MasterRunner)
        else "worker" if isinstance(environment.runner, WorkerRunner) else "standalone"
    )
    logger.info("Run context initialized", extra={"run_id": run_context.run_id})


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    run_context.user_count = environment.parsed_options.num_users or 0
    run_context.spawn_rate = environment.parsed_options.spawn_rate or 0
    run_context.run_time = environment.parsed_options.run_time or 0
    run_context.start_time = datetime.now(timezone.utc)

    metadata = get_execution_metadata()

    logger.info(
        "Execution Metadata: %s",
        metadata,
    )

    logger.info(
        "Test started",
        extra={
            "run_id": run_context.run_id,
            "target_host": run_context.target_host,
            "user_count": run_context.user_count,
            "spawn_rate": run_context.spawn_rate,
            "run_time": run_context.run_time,
            "environment": run_context.environment_name,
        },
    )


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    duration = (datetime.now(timezone.utc) - run_context.start_time).total_seconds()
    stats = environment.runner.stats

    logger.info(
        "Test finished",
        extra={
            "run_id": run_context.run_id,
            "duration_seconds": round(duration, 2),
            "total_requests": stats.num_requests,
            "total_failures": stats.num_failures,
            "avg_response_time": (
                round(stats.total.avg_response_time, 2) if stats.num_requests else 0
            ),
            "fail_ratio": (
                round(stats.total.fail_ratio, 4) if stats.num_requests else 0
            ),
            "environment": run_context.environment_name,
        },
    )


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    if exception:
        logger.warning(
            "Request failed",
            extra={
                "method": request_type,
                "endpoint": name,
                "response_time_ms": round(response_time, 2),
                "error": str(exception),
                "run_id": run_context.run_id,
            },
        )
    else:
        logger.debug(
            "Request completed",
            extra={
                "method": request_type,
                "endpoint": name,
                "response_time_ms": round(response_time, 2),
                "response_length": response_length,
                "run_id": run_context.run_id,
            },
        )
