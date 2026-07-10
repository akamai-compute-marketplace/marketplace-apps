from playwright.sync_api import expect

from regression_tests.pages.openlitespeed_wordpress.openlitespeed_wordpress_dashboard_page import (
    OpenLitespeedWordpressDashboardPage,
)
from regression_tests.pages.openlitespeed_wordpress.openlitespeed_wordpress_login_page import (
    OpenLitespeedWordpressLoginPage,
)
from regression_tests.pages.openlitespeed_wordpress.openlitespeed_wordpress_site_page import (
    OpenLitespeedWordpressSitePage,
)


def test_openlitespeed_wordpress_admin_startup(context, base_url):
    # Verifies that the app started and the admin login page loads successfully.
    login_page = OpenLitespeedWordpressLoginPage(context)
    login_page.navigate(f"{base_url}/wp-login.php")
    expect(context, "WordPress is not started").to_have_title("Log In ‹ My WP Site — WordPress")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_openlitespeed_wordpress_admin_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Wordpress admin user"]
    password = app_credentials["Wordpress admin password"]
    login_page = OpenLitespeedWordpressLoginPage(context)
    login_page.navigate(f"{base_url}/wp-login.php")
    login_page.login(username, password)
    dashboard_page = OpenLitespeedWordpressDashboardPage(context)
    expect(dashboard_page.heading, "Credentials are invalid or something went wrong.").to_be_visible()


def test_openlitespeed_wordpress_site_page(context, base_url):
    # Verifies that the public WordPress site loads successfully.
    site_page = OpenLitespeedWordpressSitePage(context)
    site_page.navigate(base_url)
    expect(context, "WordPress site did not load.").to_have_title("My WP Site")
    expect(site_page.heading, "Blog page did not render on the site homepage.").to_be_visible()
