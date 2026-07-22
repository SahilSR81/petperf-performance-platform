from locust import task


class PetTasks:

    @task
    def get_available_pets(self):
        self.client.get(
            "/pet/findByStatus",
            params={"status": "available"},
            name="GET Available Pets",
        )
