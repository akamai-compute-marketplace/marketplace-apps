class KaliLinuxService:
    """
    OS-level actions for the Kali Linux box over SSH
    """

    def __init__(self, remote_exec):
        self._run = remote_exec

    def os_release(self):
        out, _, code = self._run("cat /etc/os-release")
        return out, code

    def system_running_state(self):
        out, _, _ = self._run("systemctl is-system-running")
        return out

    def kernel(self):
        out, _, code = self._run("uname -r")
        return out, code

    def default_metapackage_version(self):
        out, _, code = self._run(
            "dpkg-query -W -f '${Version}' kali-linux-default"
        )
        return out, code
