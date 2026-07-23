from locust import task

from utils.validators import is_success, has_json_content


class PetTasks:

    @task
    def get_available_pets(self):
        with self.client.get(
            "/pet/findByStatus",
            params={"status": "available"},
            catch_response=True,
            name="GET Available Pets",
        ) as response:

            if not is_success(response):
                response.failure("Unexpected status code")
                return

            if not has_json_content(response):
                response.failure("Invalid content type")
                return

            response.success()
