import re

from playwright.sync_api import expect

from regression_tests.pages.pihole.pihole_login_page import PiholeLoginPage
from regression_tests.pages.pihole.pihole_dashboard_page import PiholeDashboardPage


def test_pihole_startup(context, base_url):
    """Verifies that Pi-hole started and the login page loads successfully."""
    login_page = PiholeLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Pi-hole login page did not load.").to_have_title(re.compile(r"Pi-hole.*"))
    expect(login_page.password_input, "Pi-hole password input did not render.").to_be_visible()
    expect(login_page.login_button, "Pi-hole login button did not render.").to_be_visible()


def test_pihole_login_status_active(context, base_url, app_credentials):
    """Verifies that the user can log in and Pi-hole reports status Active."""
    password = app_credentials["Pihole Password"]
    login_page = PiholeLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(password)
    dashboard_page = PiholeDashboardPage(context)
    expect(dashboard_page.dashboard_nav_link, "Dashboard nav link not visible after login.").to_be_visible()
    expect(dashboard_page.status_indicator, "Pi-hole status indicator not found on dashboard.").to_be_visible()
    expect(dashboard_page.status_indicator, "Pi-hole status is not Active.").to_contain_text("Active")
