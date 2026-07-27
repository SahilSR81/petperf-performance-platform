from locust import task

from utils.validators import validate_status_code


class PetReadTasks:
    @task
    def list_pets(self):
        with self.client.get("/api/v3/pet/findByStatus?status=available", catch_response=True, name="list_pets") as resp:
            validate_status_code(resp, 200)

    @task
    def find_by_status(self):
        for status in ("available", "pending", "sold"):
            with self.client.get(
                f"/api/v3/pet/findByStatus?status={status}",
                catch_response=True,
                name="find_by_status",
            ) as resp:
                validate_status_code(resp, 200)

    @task
    def get_pet_by_id(self):
        with self.client.get("/api/v3/pet/1", catch_response=True, name="get_pet_by_id") as resp:
            validate_status_code(resp, 200)
