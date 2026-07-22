from playwright.sync_api import expect

from regression_tests.pages.woocommerce.woocommerce_dashboard_page import WooCommerceDashboardPage
from regression_tests.pages.woocommerce.woocommerce_login_page import WooCommerceLoginPage
from regression_tests.pages.woocommerce.woocommerce_site_page import WooCommerceSitePage


def test_woocommerce_site_startup(context, base_url):
    # Verifies that the WooCommerce storefront started and the front page loads successfully.
    site_page = WooCommerceSitePage(context)
    site_page.navigate(base_url)
    expect(context, "WooCommerce site is not started").to_have_title("My WP Site")
    expect(site_page.shop_link, "Storefront navigation did not render.").to_be_visible()


def test_woocommerce_wp_admin_startup(context, base_url):
    # Verifies that wp-admin is reachable and redirects to the login page.
    login_page = WooCommerceLoginPage(context)
    login_page.navigate(f"{base_url}/wp-admin")
    expect(context, "wp-admin did not redirect to the login page").to_have_title(
        "Log In ‹ My WP Site — WordPress"
    )
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_woocommerce_wp_admin_login(context, base_url, app_credentials):
    # Verifies that the WordPress admin user can log in to wp-admin.
    username = app_credentials["Wordpress Admin User"]
    password = app_credentials["Wordpress Admin Password"]
    login_page = WooCommerceLoginPage(context)
    login_page.navigate(f"{base_url}/wp-admin")
    login_page.login(username, password)

    dashboard_page = WooCommerceDashboardPage(context)
    expect(dashboard_page.dashboard_heading, "Dashboard did not load after login.").to_be_visible()
