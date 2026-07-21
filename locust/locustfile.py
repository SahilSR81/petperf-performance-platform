from locust import HttpUser, task, between
from config import HOST


class PetPerfUser(HttpUser):
    wait_time = between(1, 3)
    host = HOST

    @task
    def get_available_pets(self):
        self.client.get("/pet/findByStatus?status=available")
