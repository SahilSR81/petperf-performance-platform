from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERS = int(os.getenv("USERS", 10))
SPAWN_RATE = int(os.getenv("SPAWN_RATE", 2))
RUN_TIME = os.getenv("RUN_TIME", "60s")
