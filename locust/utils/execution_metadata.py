from datetime import datetime
from platform import python_version

from .settings import BASE_URL

FRAMEWORK_VERSION = "0.1.0"


def get_execution_metadata():
    return {
        "framework": "PetPerf",
        "version": FRAMEWORK_VERSION,
        "python": python_version(),
        "target": BASE_URL,
        "executed_at": datetime.utcnow().isoformat(timespec="seconds"),
    }
