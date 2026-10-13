import json


class OpenCodeService:
    """
    CLI / headless server actions for OpenCode over SSH
    """

    CLI = "/usr/local/bin/opencode"
    URL = "http://127.0.0.1:4096"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        out, _, code = self._run(f"{self.CLI} --version </dev/null")
        return out, code

    def start_server(self):
        self._run(f"cd /tmp; setsid {self.CLI} serve >/dev/null 2>&1 </dev/null &")
        self._run(f"curl -s -o /dev/null --retry 30 --retry-connrefused --retry-delay 1 {self.URL}/global/health",
                  timeout=60)

    def health(self):
        out, _, _ = self._run(f"curl -s {self.URL}/global/health")
        return out

    def create_session(self, title):
        out, _, _ = self._run(f"curl -s -X POST -H 'Content-Type: application/json' "
                              f"-d '{{\"title\": \"{title}\"}}' {self.URL}/session")
        return json.loads(out)

    def get_session(self, session_id):
        out, _, _ = self._run(f"curl -s {self.URL}/session/{session_id}")
        return json.loads(out)

    def list_sessions(self):
        out, _, _ = self._run(f"{self.CLI} session list --format json </dev/null")
        return json.loads(out)
