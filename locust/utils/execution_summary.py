from datetime import datetime


def print_execution_summary(
    *,
    target: str,
    users: int,
    spawn_rate: int,
    run_time: str,
):

    print("\n" + "=" * 55)
    print("PetPerf Performance Summary")
    print("=" * 55)
    print(f"Target      : {target}")
    print(f"Users       : {users}")
    print(f"Spawn Rate  : {spawn_rate}")
    print(f"Run Time    : {run_time}")
    print(f"Executed At : {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 55)
