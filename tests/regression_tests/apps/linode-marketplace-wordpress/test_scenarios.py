from playwright.sync_api import expect

from regression_tests.pages.wordpress.wordpress_dashboard_page import WordPressDashboardPage
from regression_tests.pages.wordpress.wordpress_login_page import WordPressLoginPage
from regression_tests.pages.wordpress.wordpress_site_page import WordPressSitePage


def test_wordpress_site_startup(context, base_url):
    # Verifies that the WordPress site started and the front page loads successfully.
    site_page = WordPressSitePage(context)
    site_page.navigate(base_url)
    expect(context, "WordPress site is not started").to_have_title("My WP Site")
    expect(site_page.site_title_link, "Site banner did not render.").to_be_visible()


def test_wordpress_admin_startup(context, base_url):
    # Verifies that wp-admin is reachable and redirects to the login page.
    login_page = WordPressLoginPage(context)
    login_page.navigate(f"{base_url}/wp-admin")
    expect(context, "wp-admin did not redirect to the login page").to_have_title(
        "Log In ‹ My WP Site — WordPress"
    )
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_wordpress_admin_login(context, base_url, app_credentials):
    # Verifies that the WordPress admin user can log in to wp-admin.
    username = app_credentials["Wordpress Admin User"]
    password = app_credentials["Wordpress Admin Password"]
    login_page = WordPressLoginPage(context)
    login_page.navigate(f"{base_url}/wp-admin")
    login_page.login(username, password)

    dashboard_page = WordPressDashboardPage(context)
    expect(dashboard_page.dashboard_heading, "Dashboard did not load after login.").to_be_visible()
