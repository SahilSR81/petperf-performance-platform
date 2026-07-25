from locust import HttpUser, between

import hooks
from config import HOST
from tasks.pet_tasks import PetTasks


class PetPerfUser(HttpUser, PetTasks):
    host = HOST
    wait_time = between(1, 3)
