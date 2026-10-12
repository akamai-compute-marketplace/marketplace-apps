import json
import re
from playwright.sync_api import expect
from regression_tests.pages.nemoclaw.nemoclaw_tech_docs_page import NemoclawTechDocsPage
from regression_tests.services.nemoclaw.nemoclaw_service import NemoClawService


def test_nemoclaw_cli_up(remote_exec):
    # Verifies that the NemoClaw CLI is installed and runs as its service user.
    service = NemoClawService(remote_exec)
    version, error, code = service.version()

    assert code == 0, f"NemoClaw version command failed (exit {code}): {error or version}"
    assert re.fullmatch(r"nemoclaw v\d+\.\d+\.\d+[-+\w.]*", version), (
        f"unexpected NemoClaw version output: {version}"
    )


def test_nemoclaw_host_probe_is_non_mutating(remote_exec):
    # Verifies that the host readiness probe succeeds without changing the deployment.
    service = NemoClawService(remote_exec)
    output, error, code = service.host_probe()

    assert code == 0, f"NemoClaw host probe failed (exit {code}): {error or output}"
    probe = json.loads(output)
    assert probe["status"] == "supported", f"host probe did not report supported: {probe}"
    assert probe["exitCode"] == 0, f"host probe reported a failure: {probe}"
    assert probe["mutated"] is False, f"host probe unexpectedly mutated the host: {probe}"


def test_nemoclaw_tech_docs(context, techdocs_url):
    """Verify that the Nemoclaw tech docs page is accessible."""
    tech_docs_page = NemoclawTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Nemoclaw tech docs page did not load.").to_have_title("NemoClaw")
    expect(tech_docs_page.nemoclaw_header, "Nemoclaw tech docs header did not render.").to_be_visible()
