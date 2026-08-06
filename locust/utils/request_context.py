from uuid import uuid4


class RequestContext:

    def __init__(self):
        self.execution_id = str(uuid4())

    def build_headers(self):

        return {
            "X-Correlation-ID": self.execution_id,
            "User-Agent": "PetPerf/0.1.0",
        }

    def refresh(self):

        self.execution_id = str(uuid4())
