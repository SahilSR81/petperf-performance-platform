from dotenv import load_dotenv
import os

from .execution_profile import LOAD

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERS = int(os.getenv("USERS", LOAD.users))
SPAWN_RATE = int(os.getenv("SPAWN_RATE", LOAD.spawn_rate))
RUN_TIME = os.getenv("RUN_TIME", LOAD.run_time)
