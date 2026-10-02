import re

from regression_tests.services.haystack.haystack_service import HaystackService


def test_haystack_up(remote_exec):
    """Verify that the Haystack SDK is installed and importable."""
    service = HaystackService(remote_exec)
    version, code = service.version()

    assert code == 0, f"Haystack import failed (exit {code}): {version}"
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), f"unexpected Haystack version: {version}"


def test_haystack_agent_example(remote_exec):
    """Verify the guide's Agent example can run against an OpenAI-compatible endpoint."""
    service = HaystackService(remote_exec)
    out, err, code = service.run_agent_example()

    assert code == 0, f"Haystack Agent example failed (exit {code}): {err or out}"
    assert "Haystack AI is a framework." in out, f"unexpected Agent output: {out}"
