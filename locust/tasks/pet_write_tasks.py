import uuid

from locust import task

from utils.validators import validate_status_code


class PetWriteTasks:
    @task
    def add_pet(self):
        pet_id = int(uuid.uuid4().int % 100000)
        payload = {
            "id": pet_id,
            "name": f"pet-{pet_id}",
            "status": "available",
        }
        with self.client.post(
            "/api/v3/pet",
            json=payload,
            catch_response=True,
            name="add_pet",
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def update_pet(self):
        payload = {
            "id": 1,
            "name": "updated-pet",
            "status": "sold",
        }
        with self.client.put(
            "/api/v3/pet",
            json=payload,
            catch_response=True,
            name="update_pet",
        ) as resp:
            validate_status_code(resp, 200)

    @task
    def delete_pet(self):
        with self.client.delete(
            "/api/v3/pet/999999",
            catch_response=True,
            name="delete_pet",
        ) as resp:
            validate_status_code(resp, 200)
