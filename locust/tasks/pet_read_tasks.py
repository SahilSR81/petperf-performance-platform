from locust import task

from utils.data_loader import random_pet, random_status
from utils.validators import validate_status_code


class PetReadTasks:
    @task
    def list_pets(self):
        status = random_status()
        with self.client.get(f"/api/v3/pet/findByStatus?status={status}", catch_response=True, name="list_pets") as resp:
            validate_status_code(resp, 200)

    @task
    def find_by_status(self):
        status = random_status()
        with self.client.get(
            f"/api/v3/pet/findByStatus?status={status}",
            catch_response=True,
            name="find_by_status",
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def get_pet_by_id(self):
        pet = random_pet()
        with self.client.get(f"/api/v3/pet/{pet['id']}", catch_response=True, name="get_pet_by_id") as resp:
            validate_status_code(resp, 200)
