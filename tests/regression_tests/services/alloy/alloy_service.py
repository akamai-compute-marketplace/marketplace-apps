from pathlib import Path

from regression_tests.services.addon_service import AddonService

HERE = Path(__file__).parent


class AlloyService(AddonService):
    """
    Actions for the alloy add-on over SSH.
    Log shipping is tested with the add-on's pipeline (loki_pipeline.alloy) pushing to a fake Loki (fake_loki.py).
    """

    UNIT = "alloy"
    PORT = 12345
    CONFIG = "/etc/alloy/config.alloy"
    FAKE_LOKI = "/tmp/fake_loki.py"
    TEST_LOG = "/var/log/alloy_regression.log"

    def ready_status(self):
        return self.http_status("/-/ready")

    def config_valid(self):
        _, err, code = self._run(f"alloy validate {self.CONFIG}")
        return code, err

    def start_shipping_to_fake_loki(self):
        self._upload("fake_loki.py", self.FAKE_LOKI)
        self._run(f"setsid nohup python3 {self.FAKE_LOKI} > /dev/null 2>&1 < /dev/null &")
        self._upload("loki_pipeline.alloy", self.CONFIG)
        self._run(f"echo 'alloy regression test line' >> {self.TEST_LOG}")
        self._run(f"systemctl restart {self.UNIT}")
        self.wait_until(lambda: self.ready_status() == "200")

    def shipped_test_log(self):
        return self.wait_until(lambda: self.lines_read_from_test_log() > 0 and self.entries_sent() > 0)

    def lines_read_from_test_log(self):
        return self.total("loki_source_file_read_lines_total", f'path="{self.TEST_LOG}"')

    def entries_sent(self):
        return self.total("loki_write_sent_entries_total")

    def _upload(self, asset, remote_path):
        self._run(f"cat > {remote_path} <<'EOF'\n{(HERE / asset).read_text()}EOF")
