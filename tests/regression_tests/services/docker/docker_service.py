class DockerService:
    """
    CLI actions for the Docker engine over SSH
    """

    def __init__(self, remote_exec):
        self._run = remote_exec

    def unit_active(self):
        out, _, _ = self._run("systemctl is-active docker")
        return out

    def server_version(self):
        out, _, code = self._run("docker version --format '{{.Server.Version}}'")
        return out, code

    def run_hello_world(self):
        return self._run("docker run --rm hello-world")
