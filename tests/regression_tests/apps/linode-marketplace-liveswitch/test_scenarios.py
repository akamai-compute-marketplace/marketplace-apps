from playwright.sync_api import expect

from regression_tests.pages.liveswitch.liveswitch_home_page import LiveswitchHomePage
from regression_tests.pages.liveswitch.liveswitch_tech_docs_page import LiveswitchTechDocsPage


def test_liveswitch_startup(context, base_url):
    # Verifies the app started and the LiveSwitch admin console serves the initialization wizard.
    home_page = LiveswitchHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LiveSwitch Console is not started: page title not found.").to_have_title("LiveSwitch Console")
    expect(home_page.logo, "LiveSwitch logo did not render.").to_be_visible()
    expect(home_page.next_button, "Setup wizard Next button did not render.").to_be_visible()


def test_liveswitch_tech_docs(context, techdocs_url):
    """Verify that the LiveSwitch tech docs page is accessible."""
    tech_docs_page = LiveswitchTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "LiveSwitch tech docs page did not load.").to_have_title("LiveSwitch")
    expect(tech_docs_page.liveswitch_header, "LiveSwitch tech docs header did not render.").to_be_visible()
