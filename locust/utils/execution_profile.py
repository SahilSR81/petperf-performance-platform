from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionProfile:
    users: int
    spawn_rate: int
    run_time: str


SMOKE = ExecutionProfile(
    users=5,
    spawn_rate=1,
    run_time="30s",
)

LOAD = ExecutionProfile(
    users=20,
    spawn_rate=2,
    run_time="2m",
)
