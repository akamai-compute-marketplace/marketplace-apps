from playwright.sync_api import expect

from regression_tests.pages.nats.nats_monitoring_page import NatsMonitoringPage
from regression_tests.pages.nats.nats_health_probe_page import NatsHealthProbePage


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
