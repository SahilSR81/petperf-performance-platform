from locust import task

from utils.data_loader import random_pet
from utils.payload_factory import create_pet, update_pet
from utils.validators import validate_status_code


class PetWriteTasks:
    @task
    def add_pet(self):
        payload = create_pet()
        with self.client.post(
            "/api/v3/pet",
            json=payload,
            catch_response=True,
            name="add_pet",
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def update_pet(self):
        pet = random_pet()
        payload = update_pet(pet_id=pet["id"])
        with self.client.put(
            "/api/v3/pet",
            json=payload,
            catch_response=True,
            name="update_pet",
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def delete_pet(self):
        pet = random_pet()
        with self.client.delete(
            f"/api/v3/pet/{pet['id']}",
            catch_response=True,
            name="delete_pet",
        ) as resp:
            validate_status_code(resp, 200)
