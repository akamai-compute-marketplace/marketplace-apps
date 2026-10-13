from playwright.sync_api import expect
from regression_tests.pages.wazuh.wazuh_login_page import WazuhLoginPage
from regression_tests.pages.wazuh.wazuh_overview_page import WazuhOverviewPage
from regression_tests.pages.wazuh.wazuh_tech_docs_page import WazuhTechDocsPage


def test_wazuh_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = WazuhLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Wazuh is not started").to_have_title("Wazuh")
    expect(login_page.username_input, "Login form did not render.").to_be_visible(timeout=30000)


def test_wazuh_login(context, base_url, wazuh_dashboard_credentials):
    # Verifies that the admin user can log in to the Wazuh dashboard.
    login_page = WazuhLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(wazuh_dashboard_credentials["username"], wazuh_dashboard_credentials["password"])

    overview_page = WazuhOverviewPage(context)
    expect(overview_page.breadcrumb, "Dashboard did not load after login.").to_contain_text(
        "Overview", timeout=30000
    )


def test_wazuh_tech_docs(context, techdocs_url):
    """Verify that the Wazuh tech docs page is accessible."""
    tech_docs_page = WazuhTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Wazuh tech docs page title is incorrect.").to_have_title("Wazuh")
    expect(tech_docs_page.wazuh_header, "Wazuh tech docs header did not render.").to_be_visible()
