import re

from regression_tests.services.ms_agent_framework.ms_agent_framework_service import (
    MsAgentFrameworkService,
)


def test_ms_agent_framework_up(remote_exec):
    # Verifies that the Microsoft Agent Framework SDK is installed and importable.
    service = MsAgentFrameworkService(remote_exec)
    version, error, code = service.version()

    assert code == 0, f"Agent Framework import failed (exit {code}): {error or version}"
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), (
        f"unexpected Agent Framework version: {version}"
    )


def test_ms_agent_framework_agent_run(remote_exec):
    # Verifies that a minimal Agent Framework agent handles an OpenAI-compatible response.
    service = MsAgentFrameworkService(remote_exec)
    output, error, code = service.run_agent_example()

    assert code == 0, f"Agent Framework example failed (exit {code}): {error or output}"
    assert output == "Agent Framework works.", f"unexpected agent output: {output}"
