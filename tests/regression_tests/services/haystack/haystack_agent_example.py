import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        json.loads(self.rfile.read(length))
        body = json.dumps({
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "created": 0,
            "model": "Qwen/Qwen3-14B-AWQ",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Haystack AI is a framework.",
                },
                "finish_reason": "stop",
            }],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
            },
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 18000), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
agent = Agent(
    chat_generator=OpenAIChatGenerator(
        api_base_url="http://127.0.0.1:18000/v1",
        api_key=Secret.from_token("EMPTY"),
        model="Qwen/Qwen3-14B-AWQ",
    ),
    system_prompt="You are a helpful assistant that can search the web for information.",
)
result = agent.run(
    messages=[ChatMessage.from_user("What is Haystack AI?")]
)
assert result["last_message"].text == "Haystack AI is a framework."
print(result["last_message"].text)
server.shutdown()
