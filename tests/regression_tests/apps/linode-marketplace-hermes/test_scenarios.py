from regression_tests.services.hermes.hermes_service import HermesService


def test_hermes_up(remote_exec):
    # Verifies that Hermes is installed and its CLI runs.
    service = HermesService(remote_exec)
    out, code = service.version()
    assert code == 0, f"hermes CLI did not run (exit {code}): {out}"
    assert "Hermes Agent" in out, f"unexpected hermes version output: {out}"


def test_hermes_gateway_status(remote_exec):
    # Verifies that the Hermes gateway status command reports the gateway state.
    service = HermesService(remote_exec)
    out, code = service.gateway_status()
    assert code == 0, f"hermes gateway status failed (exit {code}): {out}"
    assert "Gateway is not running" in out, f"unexpected gateway status on a fresh deploy: {out}"
