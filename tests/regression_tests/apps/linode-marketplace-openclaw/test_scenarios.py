from playwright.sync_api import expect
from regression_tests.pages.openclaw.openclaw_dashboard_page import OpenClawDashboardPage


def test_openclaw_login(context, base_url, openclaw_onboarding):
    # Verifies that the OpenClaw is onboarded and can log in to dashboard with basic credentials
    dashboard_page = OpenClawDashboardPage(context)
    dashboard_page.navigate(base_url)
    expect(context, "OpenClaw is not onboarded").to_have_title("OpenClaw Control")
    expect(dashboard_page.connect_button, "Can not log in with basic auth credentials").to_be_visible()
