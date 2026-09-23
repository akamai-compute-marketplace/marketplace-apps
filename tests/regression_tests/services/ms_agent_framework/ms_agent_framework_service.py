import shlex
from pathlib import Path


class MsAgentFrameworkService:
    """Microsoft Agent Framework SDK actions executed over SSH."""

    PYTHON = "/root/.env/bin/python"
    AGENT_SCRIPT = Path(__file__).with_name("agent_example.py")

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        command = (
            f"{self.PYTHON} -c "
            "'import importlib.metadata as metadata; "
            "print(metadata.version(\"agent-framework\"))'"
        )
        return self._run(command)

    def run_agent_example(self):
        script = self.AGENT_SCRIPT.read_text(encoding="utf-8")
        command = f"{self.PYTHON} -c {shlex.quote(script)}"
        return self._run(command, timeout=60)
