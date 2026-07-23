class HermesService:
    """
    CLI / install actions for the Hermes agent over SSH
    """

    HERMES = "/opt/hermes-agent/.venv/bin/hermes"
    USER = "hermes"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def version(self):
        out, _, code = self._run(f"{self.HERMES} --version </dev/null")
        return out, code

    def gateway_status(self):
        out, _, code = self._run(
            f"runuser -l {self.USER} -c '{self.HERMES} gateway status </dev/null'"
        )
        return out, code
