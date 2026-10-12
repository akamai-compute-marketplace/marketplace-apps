class OpenFangService:
    """
    CLI / loopback API actions for OpenFang over SSH.
    The API is bound to 127.0.0.1:4200, so it is reached with curl on the box.
    """

    OPENFANG = "/opt/openfang/bin/openfang"
    LOCAL_API = "http://127.0.0.1:4200"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        out, _, code = self._run(f"{self.OPENFANG} --version")
        return out, code

    def api_get(self, path):
        out, _, _ = self._run(f"curl -s -m 10 -w '\\n%{{http_code}}' {self.LOCAL_API}{path}")
        body, _, status = out.rpartition("\n")
        return body, status
