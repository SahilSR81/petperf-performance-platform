from locust import HttpUser, between, task

from config import HOST
from tasks.pet_read_tasks import PetReadTasks
from tasks.pet_write_tasks import PetWriteTasks


class StressUser(HttpUser, PetReadTasks, PetWriteTasks):
    host = HOST
    wait_time = between(0.1, 0.5)

    @task(3)
    def aggressive_read(self):
        self.list_pets()
        self.find_by_status()
        self.get_pet_by_id()

    @task(3)
    def aggressive_write(self):
        self.add_pet()
        self.update_pet()
        self.delete_pet()
