from playwright.sync_api import expect

from regression_tests.pages.uptime_kuma.uptime_kuma_login_page import UptimeKumaLoginPage
from regression_tests.pages.uptime_kuma.uptime_kuma_dashboard_page import UptimeKumaDashboardPage
from regression_tests.pages.uptime_kuma.uptime_kuma_add_monitor_page import UptimeKumaAddMonitorPage
from regression_tests.pages.uptime_kuma.uptime_kuma_monitor_page import UptimeKumaMonitorPage


def test_uptime_kuma_startup(context, base_url):
    """Verifies that Uptime Kuma started and the login page loads successfully."""
    login_page = UptimeKumaLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Uptime Kuma login page did not load.").to_have_title("Uptime Kuma - Login")
    expect(login_page.username_input, "Uptime Kuma login form did not render.").to_be_visible()
    expect(login_page.password_input, "Uptime Kuma login form did not render.").to_be_visible()


def test_uptime_kuma_login(context, base_url, app_credentials):
    """Verifies that the admin user can log in to Uptime Kuma."""
    username = app_credentials["Uptime-Kuma Username"]
    password = app_credentials["Uptime-Kuma password"]
    login_page = UptimeKumaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = UptimeKumaDashboardPage(context)
    expect(context, "Uptime Kuma dashboard did not load after login.").to_have_title("Uptime Kuma")
    expect(dashboard_page.add_monitor_link, "Add New Monitor link not visible after login.").to_be_visible()


def test_uptime_kuma_add_monitor_status_up(context, base_url, app_credentials):
    """Verifies that a monitor pointed at the app's own URL reports status Up."""
    username = app_credentials["Uptime-Kuma Username"]
    password = app_credentials["Uptime-Kuma password"]
    login_page = UptimeKumaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = UptimeKumaDashboardPage(context)
    dashboard_page.go_to_add_monitor()
    add_monitor_page = UptimeKumaAddMonitorPage(context)
    add_monitor_page.add_monitor("Self Check", base_url)
    monitor_page = UptimeKumaMonitorPage(context)
    expect(monitor_page.monitor_heading, "Monitor page did not load after saving.").to_have_text("Self Check")
    expect(monitor_page.status_badge, "Monitor status is not Up.").to_have_text("Up", timeout=30000)
