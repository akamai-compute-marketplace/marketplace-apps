from locust import HttpUser
from config.settings import OLLAMA_BASE_URL
from tasks.ollama_tasks import LLMTaskSet
from utils.metrics import attach_listeners

class SoakTest(HttpUser):
    tasks = [LLMTaskSet]
    host = OLLAMA_BASE_URL

attach_listeners()
