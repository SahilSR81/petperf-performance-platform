from locust import HttpUser, task, between


class PetPerfUser(HttpUser):
    """
    Base user for future performance scenarios.
    """

    wait_time = between(1, 3)

    @task
    def placeholder(self):
        """
        Placeholder task.
        Real performance scenarios will be implemented
        in upcoming milestones.
        """
        pass
