from playwright.sync_api import expect

from regression_tests.pages.haltdos.haltdos_login_page import HaltdosLoginPage


def test_haltdos_login(context, base_url):
    # Verifies that the Haltdos is started and user can log in with basic auth credentials
    login_page = HaltdosLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Haltdos is not started").to_have_title("Haltdos Management Console")
    expect(login_page.full_name_field, "Can not log in with basic auth credentials").to_be_visible()
