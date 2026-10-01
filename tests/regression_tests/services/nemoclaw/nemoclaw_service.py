import shlex


class NemoClawService:
    """NemoClaw CLI actions executed as the deployed service user over SSH."""

    CLI = "/usr/local/bin/nemoclaw"
    USER = "nemoclaw"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def _run_cli(self, *arguments):
        command = (
            f"NEMO_UID=$(id -u {self.USER}); "
            "export XDG_RUNTIME_DIR=/run/user/$NEMO_UID "
            "DBUS_SESSION_BUS_ADDRESS=unix:path=$XDG_RUNTIME_DIR/bus; "
            f"runuser -u {self.USER} -- env "
            'XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" '
            'DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" '
            f"{self.CLI} {shlex.join(arguments)}"
        )
        return self._run(command)

    def version(self):
        return self._run_cli("--version")

    def host_probe(self):
        return self._run_cli("host", "probe", "--json")
