from locust import HttpUser, LoadTestShape
from config.settings import OLLAMA_BASE_URL
from tasks.ollama_tasks import LLMTaskSet
from utils.metrics import attach_listeners


class ConcurrencyShape(LoadTestShape):
    stages = [
        {"duration": 300,  "users": 1,  "spawn_rate": 1},
        {"duration": 600,  "users": 5,  "spawn_rate": 1},
        {"duration": 900,  "users": 10, "spawn_rate": 1},
        {"duration": 1200, "users": 15, "spawn_rate": 1},
    ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
        return None

class ConcurrencyTest(HttpUser):
    tasks = [LLMTaskSet]
    host = OLLAMA_BASE_URL

attach_listeners()
