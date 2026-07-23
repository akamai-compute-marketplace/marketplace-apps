import shlex


class MemgraphService:
    """
    Client actions for the Memgraph graph database over SSH.

    Bolt is bound on all interfaces but firewalled (UFW allows SSH only by default),
    so the mgconsole client runs on the box via remote_exec. Bolt requires SSL.
    """

    UNIT = "memgraph"
    BOLT_PORT = 7687

    def __init__(self, remote_exec):
        self._run = remote_exec

    def unit_active(self):
        out, _, _ = self._run(f"systemctl is-active {self.UNIT}")
        return out

    def bolt_listener(self):
        out, _, _ = self._run(f"ss -tlnH 'sport = :{self.BOLT_PORT}'")
        return out

    def cypher(self, username, password, query):
        cmd = (
            f"printf '%s\\n' {shlex.quote(query)} | mgconsole "
            f"--username {shlex.quote(username)} "
            f"--password {shlex.quote(password)} "
            f"--use-ssl=true --output-format=csv"
        )
        return self._run(cmd)
