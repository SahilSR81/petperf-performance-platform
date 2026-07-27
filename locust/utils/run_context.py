from datetime import datetime


class RunContext:
    def __init__(self) -> None:
        self.run_id: str = ""
        self.target_host: str = ""
        self.user_count: int = 0
        self.spawn_rate: int = 0
        self.run_time: int = 0
        self.environment_name: str = ""
        self.start_time: datetime | None = None
