from locust import LoadTestShape


class StepLoadShape(LoadTestShape):
    step_time = 60
    step_users = 10
    spawn_rate = 5
    max_users = 100

    def tick(self):
        run_time = self.get_run_time()
        step_number = int(run_time / self.step_time) + 1
        if step_number * self.step_users > self.max_users:
            return None
        return (step_number * self.step_users, self.spawn_rate)


class RampUpShape(LoadTestShape):
    target_users = 50
    ramp_up_time = 120
    spawn_rate = 5

    def tick(self):
        run_time = self.get_run_time()
        if run_time >= self.ramp_up_time:
            return (self.target_users, self.spawn_rate)
        users = int((run_time / self.ramp_up_time) * self.target_users)
        return (max(users, 1), self.spawn_rate)


class SpikeShape(LoadTestShape):
    baseline_users = 10
    spike_users = 100
    spike_duration = 30
    total_duration = 180

    def tick(self):
        run_time = self.get_run_time()
        if run_time > self.total_duration:
            return None
        if run_time < 30:
            return (self.baseline_users, 2)
        elif run_time < 60:
            return (self.baseline_users, 2)
        elif run_time < 90:
            return (self.spike_users, 20)
        elif run_time < 120:
            return (self.baseline_users, 2)
        elif run_time < 150:
            return (self.spike_users, 20)
        else:
            return (self.baseline_users, 2)


class EnduranceShape(LoadTestShape):
    target_users = 30
    spawn_rate = 5
    duration = 1800

    def tick(self):
        run_time = self.get_run_time()
        if run_time >= self.duration:
            return None
        if run_time < 60:
            return (int((run_time / 60) * self.target_users), self.spawn_rate)
        return (self.target_users, self.spawn_rate)
