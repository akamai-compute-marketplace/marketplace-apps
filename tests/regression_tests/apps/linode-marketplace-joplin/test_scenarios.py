from playwright.sync_api import expect

from regression_tests.pages.joplin.joplin_login_page import JoplinLoginPage
from regression_tests.pages.joplin.joplin_dashboard_page import JoplinDashboardPage


def test_joplin_startup(context, base_url):
    # Verifies the app started and the Joplin Server login page loads successfully.
    login_page = JoplinLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Joplin Server is not started: page title not found.").to_have_title("Joplin Server - Login")
    expect(login_page.heading, "Login heading did not render.").to_be_visible()
    expect(login_page.email_input, "Email input did not render.").to_be_visible()


def test_joplin_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with provided credentials.
    email = app_credentials["Joplin Login"]
    password = app_credentials["Joplin Password"]
    login_page = JoplinLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)
    dashboard_page = JoplinDashboardPage(context)
    expect(context, "Admin dashboard did not load after login.").to_have_title("Joplin Server - Admin dashboard")
    expect(dashboard_page.heading, "Dashboard heading not visible after login.").to_be_visible()
    expect(dashboard_page.logout_button, "Logout button not visible — login may have failed.").to_be_visible()
