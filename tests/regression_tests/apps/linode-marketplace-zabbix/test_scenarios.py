from playwright.sync_api import expect

from regression_tests.pages.zabbix.zabbix_login_page import ZabbixLoginPage
from regression_tests.pages.zabbix.zabbix_dashboard_page import ZabbixDashboardPage


def test_zabbix_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = ZabbixLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Zabbix is not started").to_have_title("zabbix-server: Zabbix")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_zabbix_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in to the Zabbix dashboard.
    username = app_credentials["Zabbix Admin GUI Username"]
    password = app_credentials["Zabbix Admin GUI Password"]
    login_page = ZabbixLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    dashboard_page = ZabbixDashboardPage(context)
    expect(dashboard_page.global_view_heading, "Dashboard did not load after login.").to_be_visible()


def test_zabbix_server_is_running(context, base_url, app_credentials):
    # Verifies that the Zabbix server process is reported as running on the dashboard.
    username = app_credentials["Zabbix Admin GUI Username"]
    password = app_credentials["Zabbix Admin GUI Password"]
    login_page = ZabbixLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    dashboard_page = ZabbixDashboardPage(context)
    expect(
        dashboard_page.system_information_heading, "System information widget did not render."
    ).to_be_visible()
    expect(
        dashboard_page.server_running_value, "Zabbix server is not reported as running."
    ).to_have_text("Yes")
