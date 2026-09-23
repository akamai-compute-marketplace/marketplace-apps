import shlex
from pathlib import Path


class HaystackService:
    """Haystack SDK actions executed over SSH."""

    PYTHON = "/root/.env/bin/python"
    AGENT_SCRIPT = Path(__file__).with_name("haystack_agent_example.py")

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        out, _, code = self._run(
            f"{self.PYTHON} -c 'import haystack; print(haystack.__version__)'"
        )
        return out, code

    def run_agent_example(self):
        script = self.AGENT_SCRIPT.read_text(encoding="utf-8")
        command = f"{self.PYTHON} -c {shlex.quote(script)}"
        return self._run(command, timeout=60)
