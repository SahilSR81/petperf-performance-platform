import logging
import os
from threading import Thread

from prometheus_client import start_http_server, push_to_gateway

logger = logging.getLogger(__name__)

PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9091"))
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "")


def start_metrics_server() -> None:
    start_http_server(PROMETHEUS_PORT)
    logger.info("Prometheus metrics endpoint exposed on port %s", PROMETHEUS_PORT)


def start_metrics_exporter() -> None:
    if PUSHGATEWAY_URL:
        logger.info("Using Pushgateway at %s", PUSHGATEWAY_URL)
    else:
        thread = Thread(target=start_metrics_server, daemon=True)
        thread.start()
