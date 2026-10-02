class MinecraftService:
    """Minecraft service actions executed over SSH."""

    USER = "linuxgsm"
    UNIT = "mcserver"
    PORT = "25565"

    def __init__(self, remote_exec):
        self._run = remote_exec

    def status(self):
        command = (
            f"su - {self.USER} -c "
            f"'XDG_RUNTIME_DIR=/run/user/$(id -u) "
            f"DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus "
            f"systemctl --user status {self.UNIT} --no-pager'"
        )
        return self._run(command)

    def listening_ports(self):
        return self._run(f"ss -ltnup | grep ':{self.PORT} '")
