from playwright.sync_api import expect
from regression_tests.services.hermes.hermes_service import HermesService
from regression_tests.pages.hermes.hermes_tech_docs_page import HermesTechDocsPage


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


def test_hermes_tech_docs(context, techdocs_url):
    """Verify that the Hermes tech docs page is accessible."""
    tech_docs_page = HermesTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Hermes tech docs page did not load.").to_have_title("Hermes")
    expect(tech_docs_page.hermes_header, "Hermes tech docs header did not render.").to_be_visible()
