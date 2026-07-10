from playwright.sync_api import expect

from regression_tests.pages.openlitespeed_cpanel.openlitespeed_cpanel_default_page import (
    OpenlitespeedCpanelDefaultPage,
)
from regression_tests.pages.openlitespeed_cpanel.openlitespeed_cpanel_litespeed_home_page import (
    OpenlitespeedCpanelLitespeedHomePage,
)
from regression_tests.pages.openlitespeed_cpanel.openlitespeed_cpanel_litespeed_login_page import (
    OpenlitespeedCpanelLitespeedLoginPage,
)
from regression_tests.pages.openlitespeed_cpanel.openlitespeed_cpanel_whm_initial_setup_page import (
    OpenlitespeedCpanelWhmInitialSetupPage,
)
from regression_tests.pages.openlitespeed_cpanel.openlitespeed_cpanel_whm_login_page import (
    OpenlitespeedCpanelWhmLoginPage,
)


def test_openlitespeed_cpanel_whm_startup(context, base_url):
    """Verifies that WHM started and the login page loads successfully."""
    login_page = OpenlitespeedCpanelWhmLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "WHM login page did not load — app may not have started.").to_have_title("WHM Login")
    expect(login_page.username_input, "Username input was not visible on the WHM login page.").to_be_visible()
    expect(login_page.password_input, "Password input was not visible on the WHM login page.").to_be_visible()


def test_openlitespeed_cpanel_whm_login(context, base_url, app_credentials):
    """Verifies that the root user can log in to WHM with the Linode root password."""
    username = app_credentials["username"]
    password = app_credentials["password"]

    login_page = OpenlitespeedCpanelWhmLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    setup_page = OpenlitespeedCpanelWhmInitialSetupPage(context)
    expect(
        setup_page.legal_documents_heading,
        "WHM Initial Setup Wizard did not load after login — login may have failed.",
    ).to_be_visible(timeout=30000)


def test_openlitespeed_cpanel_litespeed_webadmin_startup(context, litespeed_base_url):
    """Verifies that the LiteSpeed WebAdmin console started and its login page loads."""
    login_page = OpenlitespeedCpanelLitespeedLoginPage(context)
    login_page.navigate(litespeed_base_url)
    expect(
        context, "LiteSpeed WebAdmin login page did not load — lsws may not have started."
    ).to_have_title("- LiteSpeed WebAdmin Console")
    expect(
        login_page.username_input, "Username input was not visible on the LiteSpeed WebAdmin login page."
    ).to_be_visible()
    expect(
        login_page.password_input, "Password input was not visible on the LiteSpeed WebAdmin login page."
    ).to_be_visible()


def test_openlitespeed_cpanel_litespeed_webadmin_login(context, litespeed_base_url, litespeed_credentials):
    """Verifies that the generated admin account can log in to the LiteSpeed WebAdmin console."""
    username = litespeed_credentials["LiteSpeed WebAdmin Username"]
    password = litespeed_credentials["LiteSpeed WebAdmin Password"]

    login_page = OpenlitespeedCpanelLitespeedLoginPage(context)
    login_page.navigate(litespeed_base_url)
    login_page.login(username, password)

    home_page = OpenlitespeedCpanelLitespeedHomePage(context)
    expect(
        home_page.home_heading,
        "LiteSpeed WebAdmin Home page did not load after login — login may have failed.",
    ).to_be_visible(timeout=30000)
    expect(
        home_page.log_off_link, "Log Off link was not visible after logging in to LiteSpeed WebAdmin."
    ).to_be_visible()


def test_openlitespeed_cpanel_default_web_page(context, http_base_url):
    """Verifies that LiteSpeed (not Apache) serves the stock cPanel default web page on port 80."""
    default_page = OpenlitespeedCpanelDefaultPage(context)
    default_page.navigate(http_base_url)
    expect(context, "Default web page did not load on port 80.").to_have_title("Default Web Site Page")
    expect(
        default_page.sorry_text, "Expected 'SORRY!' placeholder text was not visible on the default web page."
    ).to_be_visible()
