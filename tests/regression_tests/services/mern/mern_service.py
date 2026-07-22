import shlex


class MernService:
    """
    Backend actions for the MERN stack
    """

    MONGO_PORT = 27017

    def __init__(self, remote_exec=None, http_session=None, base_url=None):
        self._run = remote_exec
        self._http = http_session
        self._base = base_url.rstrip("/") if base_url else None

    def unit_active(self, unit):
        out, _, _ = self._run(f"systemctl is-active {unit}")
        return out

    def listening_ports(self):
        out, _, _ = self._run("ss -tlnH")
        return out

    def mongo_eval(self, username, password, database, script):
        cmd = (
            f"mongosh --quiet -u {shlex.quote(username)} -p {shlex.quote(password)} "
            f"--authenticationDatabase admin {shlex.quote(database)} "
            f"--eval {shlex.quote(script)}"
        )
        return self._run(cmd)

    def mongo_eval_unauthenticated(self, script):
        cmd = f"mongosh --quiet --eval {shlex.quote(script)}"
        return self._run(cmd)

    def api_get(self, path):
        return self._http.get(f"{self._base}{path}", timeout=30)
