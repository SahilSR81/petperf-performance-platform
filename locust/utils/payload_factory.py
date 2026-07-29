import uuid

from utils.data_loader import random_status


def create_pet() -> dict:
    pet_id = int(uuid.uuid4().int % 100000)
    return {
        "id": pet_id,
        "name": f"pet-{pet_id}",
        "status": random_status(),
    }


def update_pet(pet_id: int = 1) -> dict:
    return {
        "id": pet_id,
        "name": "updated-pet",
        "status": random_status(),
    }


def delete_pet_payload(pet_id: int = 999999) -> dict:
    return {"id": pet_id}
