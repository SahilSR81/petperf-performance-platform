from locust import task

from utils.data_loader import random_pet, random_status
from utils.request_names import RequestName, get_request_name
from utils.validators import validate_status_code


class PetReadTasks:
    @task
    def list_pets(self):
        status = random_status()
        with self.client.get(
            f"/api/v3/pet/findByStatus?status={status}",
            catch_response=True,
            name=get_request_name(RequestName.GET_AVAILABLE_PETS),
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def find_by_status(self):
        status = random_status()
        with self.client.get(
            f"/api/v3/pet/findByStatus?status={status}",
            catch_response=True,
            name=get_request_name(RequestName.GET_AVAILABLE_PETS),
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def get_pet_by_id(self):
        pet = random_pet()
        with self.client.get(
            f"/api/v3/pet/{pet['id']}",
            catch_response=True,
            name=get_request_name(RequestName.GET_PET_BY_ID),
        ) as resp:
            validate_status_code(resp, 200)
