from playwright.sync_api import expect
from regression_tests.pages.nats.nats_monitoring_page import NatsMonitoringPage
from regression_tests.pages.nats.nats_health_probe_page import NatsHealthProbePage
from regression_tests.pages.nats.nats_tech_docs_page import NatsTechDocsPage


def test_nats_startup(context, base_url):
    # Verifies that the NATS monitoring dashboard started and loads successfully.
    monitoring_page = NatsMonitoringPage(context)
    monitoring_page.navigate(base_url)
    expect(monitoring_page.health_probe_link, "NATS monitoring dashboard did not render.").to_be_visible()


def test_nats_health_probe(context, base_url):
    # Verifies that the NATS health probe endpoint reports the server as healthy.
    health_probe_page = NatsHealthProbePage(context)
    health_probe_page.navigate(f"{base_url}/healthz")
    expect(
        health_probe_page.status_text,
        "NATS health probe did not report an OK status.",
    ).to_contain_text('"status":"ok"')


def test_nats_tech_docs(context, techdocs_url):
    """Verify that the NATS tech docs page is accessible."""
    tech_docs_page = NatsTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "NATS tech docs page did not load.").to_have_title("NATS")
    expect(tech_docs_page.nats_header, "NATS tech docs header did not render.").to_be_visible()
