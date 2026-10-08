import re

from playwright.sync_api import expect
from regression_tests.services.haystack.haystack_service import HaystackService
from regression_tests.pages.haystack.haystack_tech_docs_page import HaystackTechDocsPage


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


def test_haystack_tech_docs(context, techdocs_url):
    """Verify that the Haystack tech docs page is accessible."""
    tech_docs_page = HaystackTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Haystack tech docs page did not load.").to_have_title("Haystack")
    expect(tech_docs_page.haystack_header, "Haystack tech docs header did not render.").to_be_visible()
