import time

from playwright.sync_api import expect

from regression_tests.pages.cyberpanel.cyberpanel_login_page import CyberPanelLoginPage
from regression_tests.pages.cyberpanel.cyberpanel_dashboard_page import CyberPanelDashboardPage
from regression_tests.pages.cyberpanel.cyberpanel_create_website_page import CyberPanelCreateWebsitePage


def test_cyberpanel_startup(context, base_url):
    """Verifies that CyberPanel started and the login page loads successfully."""
    login_page = CyberPanelLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "CyberPanel login page did not load — app may not have started.").to_have_title("Login - CyberPanel")
    expect(login_page.username_input, "Username input was not visible on the login page.").to_be_visible()
    expect(login_page.password_input, "Password input was not visible on the login page.").to_be_visible()


def test_cyberpanel_login(context, base_url, app_credentials):
    """Verifies that the admin user can log in with credentials"""
    username = "admin"
    password = app_credentials["admin_pass"]
    login_page = CyberPanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = CyberPanelDashboardPage(context)
    expect(dashboard_page.dashboard_menu_item, "Dashboard menu item was not visible after login — login may have failed.").to_be_visible()


def test_cyberpanel_create_website(context, base_url, app_credentials):
    """Verifies that an admin user can create a new website via the Create Website form."""
    username = "admin"
    password = app_credentials["admin_pass"]

    # Log in first
    login_page = CyberPanelLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    dashboard_page = CyberPanelDashboardPage(context)
    expect(dashboard_page.dashboard_menu_item, "Login did not succeed — cannot proceed to create website.").to_be_visible()

    # Navigate to the create website page
    create_page = CyberPanelCreateWebsitePage(context)
    create_page.navigate(f"{base_url}/websites/createWebsite")

    expect(create_page.domain_input, "Create Website form did not load — domain input not visible.").to_be_visible()

    # Use a unique domain per run so the test is safe to re-run on the same VM
    unique_domain = f"testsite-{int(time.time())}.example.com"

    # Fill in the form and submit
    create_page.create_website(
        domain=unique_domain,
        email=f"admin@{unique_domain}",
    )

    # CyberPanel creates the website asynchronously; it typically takes ~20 s
    expect(create_page.success_alert, "Website was not created successfully — success alert did not appear.").to_be_visible(timeout=60000)
