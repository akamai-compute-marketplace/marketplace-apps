import time
from pathlib import Path

from regression_tests.services.addon_service import AddonService

TRACE_TEMPLATE = Path(__file__).parent / "trace.json"


class OtelcolService(AddonService):
    """
    Actions for the opentelemetry_collector add-on over SSH
    """

    UNIT = "otelcol"
    OTLP_GRPC_PORT = 4317
    PORT = OTLP_HTTP_PORT = 4318
    SELF_METRICS_PORT = 8888

    def listening_ports(self):
        out, _, _ = self._run("ss -H -ltn")
        return out

    def send_trace(self):
        now = time.time_ns()
        payload = TRACE_TEMPLATE.read_text().replace("@START@", str(now - 1_000_000)).replace("@END@", str(now))
        out, _, _ = self._run(
            "curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' "
            f"-d '{payload}' http://127.0.0.1:{self.OTLP_HTTP_PORT}/v1/traces"
        )
        return out

    def accepted_spans(self):
        return self.total("otelcol_receiver_accepted_spans", 'receiver="otlp"', self.SELF_METRICS_PORT)
