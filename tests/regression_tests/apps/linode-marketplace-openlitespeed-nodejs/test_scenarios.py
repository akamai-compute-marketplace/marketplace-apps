from playwright.sync_api import expect

from regression_tests.pages.openlitespeed_nodejs.openlitespeed_nodejs_dashboard_page import (
    OpenLiteSpeedNodeJsDashboardPage,
)
from regression_tests.pages.openlitespeed_nodejs.openlitespeed_nodejs_home_page import (
    OpenLiteSpeedNodeJsHomePage,
)
from regression_tests.pages.openlitespeed_nodejs.openlitespeed_nodejs_login_page import (
    OpenLiteSpeedNodeJsLoginPage,
)


def test_openlitespeed_nodejs_startup(context, base_url):
    # Verifies that the sample Node.js application displays its welcome message.
    home_page = OpenLiteSpeedNodeJsHomePage(context)
    home_page.navigate(base_url)
    expect(home_page.welcome_message, "OpenLiteSpeed Node.js welcome message did not render.").to_be_visible()


def test_openlitespeed_nodejs_admin_startup(context, admin_url):
    # Verifies that the OpenLiteSpeed WebAdmin login page loads successfully.
    login_page = OpenLiteSpeedNodeJsLoginPage(context)
    login_page.navigate(admin_url)
    expect(context, "OpenLiteSpeed WebAdmin did not start.").to_have_title("OpenLiteSpeed WebAdmin Console")
    expect(login_page.username_input, "WebAdmin login form did not render.").to_be_visible()


def test_openlitespeed_nodejs_admin_login(context, admin_url, app_credentials):
    # Verifies that WebAdmin accepts the generated credentials and opens its dashboard.
    login_page = OpenLiteSpeedNodeJsLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(
        app_credentials["WebAdmin Username"],
        app_credentials["WebAdmin Password"],
    )
    dashboard_page = OpenLiteSpeedNodeJsDashboardPage(context)
    expect(dashboard_page.dashboard_heading, "OpenLiteSpeed WebAdmin dashboard did not load after login.").to_be_visible()
