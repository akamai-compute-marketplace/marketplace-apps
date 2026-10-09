from playwright.sync_api import expect
from regression_tests.pages.openclaw.openclaw_dashboard_page import OpenClawDashboardPage
from regression_tests.pages.openclaw.openclaw_tech_docs_page import OpenclawTechDocsPage


def test_openclaw_login(context, base_url, openclaw_onboarding):
    # Verifies that the OpenClaw is onboarded and can log in to dashboard with basic credentials
    dashboard_page = OpenClawDashboardPage(context)
    dashboard_page.navigate(base_url)
    expect(context, "OpenClaw is not onboarded").to_have_title("OpenClaw Control")
    expect(dashboard_page.connect_button, "Can not log in with basic auth credentials").to_be_visible()


def test_openclaw_tech_docs(context, techdocs_url):
    """Verify that the OpenClaw tech docs page is accessible."""
    tech_docs_page = OpenclawTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenClaw tech docs page did not load.").to_have_title("OpenClaw")
    expect(tech_docs_page.openclaw_header, "OpenClaw tech docs header did not render.").to_be_visible()
