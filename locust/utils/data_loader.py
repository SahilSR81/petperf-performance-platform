import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> list | dict:
    path = DATA_DIR / filename
    with open(path) as f:
        return json.load(f)


def load_payload(filename: str) -> list | dict:
    return load_json(filename)


def random_pet() -> dict:
    pets = load_json("pets.json")
    return random.choice(pets)


def random_status() -> str:
    statuses = load_json("pet_status.json")
    return random.choice(statuses)
