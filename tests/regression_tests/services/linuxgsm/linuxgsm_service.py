class LinuxGSMService:
    """
    CLI actions for the LinuxGSM game-server manager over SSH
    """

    USER = "linuxgsm"
    HOME = "/home/linuxgsm"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def _as_user(self, args=""):
        return self._run(
            f"runuser -l {self.USER} -c 'cd {self.HOME} && ./linuxgsm.sh {args}'"
        )

    def version(self):
        out, err, code = self._as_user()
        return f"{out}\n{err}", code

    def list_servers(self):
        out, err, code = self._as_user("list")
        return f"{out}\n{err}", code
