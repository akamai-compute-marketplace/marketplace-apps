import re

from playwright.sync_api import expect

from regression_tests.pages.ms_agent_framework.ms_agent_framework_tech_docs_page import MsAgentFrameworkTechDocsPage

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


def test_ms_agent_framework_tech_docs(context, techdocs_url):
    """Verify that the Microsoft Agent Framework tech docs page is accessible."""
    tech_docs_page = MsAgentFrameworkTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Microsoft Agent Framework tech docs page did not load.").to_have_title("Microsoft Agent Framework")
    expect(tech_docs_page.ms_agent_framework_header, "Microsoft Agent Framework tech docs header did not render.").to_be_visible()
