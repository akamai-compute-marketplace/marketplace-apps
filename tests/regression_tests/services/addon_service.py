import time


class AddonService:
    """
    Common checks for monitoring add-ons that run as a systemd unit and expose HTTP metrics.
    Subclasses set UNIT and PORT.
    """

    UNIT = None
    PORT = None

    def __init__(self, remote_exec):
        self._run = remote_exec

    def unit_active(self):
        out, _, _ = self._run(f"systemctl is-active {self.UNIT}")
        return out

    def unit_enabled(self):
        out, _, _ = self._run(f"systemctl is-enabled {self.UNIT}")
        return out

    def process_user(self):
        out, _, _ = self._run(f"ps -o user:32= -C {self.UNIT}")
        return out

    def http_status(self, path, port=None):
        out, _, _ = self._run(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:{port or self.PORT}{path}")
        return out

    def metrics(self, port=None):
        out, err, code = self._run(f"curl -sf http://127.0.0.1:{port or self.PORT}/metrics")
        if code != 0:
            raise RuntimeError(f"metrics endpoint unreachable (exit {code}): {err}")
        return out.splitlines()

    def line(self, prefix, port=None):
        return next((line for line in self.metrics(port) if line.startswith(prefix)), None)

    def value(self, series, port=None):
        found = self.line(series + " ", port)
        return float(found.rsplit(" ", 1)[1]) if found else None

    def total(self, metric, label="", port=None):
        return sum(
            float(line.rsplit(" ", 1)[1])
            for line in self.metrics(port)
            if line.startswith(metric) and label in line
        )

    @staticmethod
    def wait_until(condition, timeout=60, interval=3):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if condition():
                return True
            time.sleep(interval)
        return False
