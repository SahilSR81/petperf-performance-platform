from locust import HttpUser, between, task

from config import HOST
from tasks.pet_read_tasks import PetReadTasks
from tasks.pet_write_tasks import PetWriteTasks


class LoadUser(HttpUser, PetReadTasks, PetWriteTasks):
    host = HOST
    wait_time = between(0.5, 2)

    @task(5)
    def read_flow(self):
        self.list_pets()
        self.find_by_status()
        self.get_pet_by_id()

    @task(2)
    def write_flow(self):
        self.add_pet()
        self.update_pet()

    @task(1)
    def delete_flow(self):
        self.delete_pet()
