import asyncio
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)

        if self.path != "/v1/responses":
            self.send_response(404)
            self.end_headers()
            return

        response = {
            "id": "resp_regression",
            "object": "response",
            "created_at": 0,
            "status": "completed",
            "model": "test-model",
            "output": [
                {
                    "type": "message",
                    "id": "msg_regression",
                    "status": "completed",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "output_text",
                            "text": "Agent Framework works.",
                            "annotations": [],
                        }
                    ],
                }
            ],
            "parallel_tool_calls": False,
            "tool_choice": "auto",
            "temperature": 1.0,
            "top_p": 1.0,
            "usage": {"input_tokens": 1, "output_tokens": 4, "total_tokens": 5},
        }
        encoded = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 18000), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

client = OpenAIChatClient(
    model="test-model",
    api_key="EMPTY",
    base_url="http://127.0.0.1:18000/v1",
)
agent = Agent(client=client, instructions="Answer briefly.")
response = asyncio.run(agent.run("Say hello."))
print(response.text)
server.shutdown()
