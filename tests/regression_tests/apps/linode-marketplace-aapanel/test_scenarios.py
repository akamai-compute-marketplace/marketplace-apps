from playwright.sync_api import expect

from regression_tests.pages.aapanel.aapanel_dashboard_page import AaPanelDashboardPage
from regression_tests.pages.aapanel.aapanel_login_page import AaPanelLoginPage


def test_aapanel_startup(context, base_url):
    """Verify that aaPanel started and its login page is available."""
    login_page = AaPanelLoginPage(context)
    login_page.navigate(base_url)

    expect(context, "aaPanel login page did not load.").to_have_title("aaPanel Linux panel")
    expect(login_page.login_button, "aaPanel Login button did not render.").to_be_visible()


def test_aapanel_login(context, base_url, app_credentials):
    """Verify aaPanel login and complete its one-time setup dialogs."""
    login_page = AaPanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(
        app_credentials["aaPanel Username"],
        app_credentials["aaPanel Password"],
    )
    login_page.complete_first_login_setup()
    dashboard_page = AaPanelDashboardPage(context)
    expect(context, "aaPanel home page did not load after login.").to_have_title("aaPanel Linux panel - Home")
    expect(dashboard_page.home_navigation, "aaPanel Home navigation did not appear after login.").to_be_visible()
