from playwright.sync_api import expect

from regression_tests.pages.cloudron.cloudron_setup_page import CloudronSetupPage


def test_cloudron_startup(context, base_url):
    # Verifies that Cloudron started and the initial domain setup wizard is shown.
    setup_page = CloudronSetupPage(context)
    setup_page.navigate(base_url)
    expect(context, "Cloudron is not started").to_have_title("Domain Setup")
    expect(setup_page.heading, "Domain Setup wizard did not render.").to_be_visible()
    expect(setup_page.domain_input, "Domain input field did not render.").to_be_visible()
