from locust import HttpUser, between, task

from config import HOST
from tasks.pet_read_tasks import PetReadTasks
from tasks.pet_write_tasks import PetWriteTasks


class SoakUser(HttpUser, PetReadTasks, PetWriteTasks):
    host = HOST
    wait_time = between(2, 5)

    @task(8)
    def read_flow(self):
        self.list_pets()
        self.find_by_status()
        self.get_pet_by_id()

    @task(1)
    def write_flow(self):
        self.add_pet()
