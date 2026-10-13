import uuid
import pytest
from playwright.sync_api import expect
from regression_tests.pages.opencode.opencode_tech_docs_page import OpenCodeTechDocsPage
from regression_tests.services.opencode.opencode_service import OpenCodeService


def test_opencode_up(remote_exec):
    # Verifies that OpenCode is installed and its CLI runs.
    service = OpenCodeService(remote_exec)
    out, code = service.version()
    assert code == 0, f"opencode CLI did not run (exit {code}): {out}"


def test_opencode_server_reports_healthy(remote_exec, opencode_server):
    # Verifies that the headless server serves its health endpoint and matches the CLI version.
    service = OpenCodeService(remote_exec)
    body = service.health()
    version, _ = service.version()

    assert '"healthy":true' in body, f"server did not report healthy: {body}"
    assert f'"version":"{version}"' in body, f"server version does not match CLI {version!r}: {body}"


def test_opencode_session_roundtrip(remote_exec, opencode_server):
    # Verifies that a session created over the API reads back from the API and the CLI.
    service = OpenCodeService(remote_exec)
    title = f"regression-{uuid.uuid4().hex[:8]}"

    created = service.create_session(title)
    fetched = service.get_session(created["id"])
    cli_sessions = service.list_sessions()

    assert fetched["title"] == title, f"session did not read back from the API: {fetched}"
    assert any(s["id"] == created["id"] and s["title"] == title for s in cli_sessions), \
        f"session {created['id']} missing from 'opencode session list': {cli_sessions}"


@pytest.mark.xfail(reason="Tech docs page is not ready yet")
def test_opencode_tech_docs(context, techdocs_url):
    """Verify that the OpenCode tech docs page is accessible."""
    tech_docs_page = OpenCodeTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenCode tech docs title did not match.").to_have_title("OpenCode")
    expect(tech_docs_page.opencode_header, "OpenCode tech docs header did not render.").to_be_visible()
