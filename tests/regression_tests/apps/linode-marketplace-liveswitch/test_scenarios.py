from playwright.sync_api import expect

from regression_tests.pages.liveswitch.liveswitch_home_page import LiveswitchHomePage


def test_liveswitch_startup(context, base_url):
    # Verifies the app started and the LiveSwitch admin console serves the initialization wizard.
    home_page = LiveswitchHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LiveSwitch Console is not started: page title not found.").to_have_title("LiveSwitch Console")
    expect(home_page.logo, "LiveSwitch logo did not render.").to_be_visible()
    expect(home_page.next_button, "Setup wizard Next button did not render.").to_be_visible()
