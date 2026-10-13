from playwright.sync_api import expect

from regression_tests.pages.beef.beef_login_page import BeefLoginPage
from regression_tests.pages.beef.beef_dashboard_page import BeefDashboardPage
from regression_tests.pages.beef.beef_tech_docs_page import BeefTechDocsPage


def test_beef_startup(context, base_url):
    # Verifies that BeEF started and the authentication page loads.
    login_page = BeefLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "BeEF is not started").to_have_title("BeEF Authentication")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_beef_login(context, base_url, app_credentials):
    # Verifies that a user can log in with the provided credentials.
    username = app_credentials["BeEF Login"]
    password = app_credentials["BeEF Password"]
    login_page = BeefLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = BeefDashboardPage(context)
    expect(dashboard_page.logout_link, "Dashboard did not load after login.").to_be_visible()


def test_beef_tech_docs(context, techdocs_url):
    """Verify that the BeEF tech docs page is accessible."""
    tech_docs_page = BeefTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "BeEF tech docs page did not load.").to_have_title("BeEF")
    expect(tech_docs_page.beef_header, "BeEF tech docs header did not render.").to_be_visible()
