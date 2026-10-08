from playwright.sync_api import expect

from regression_tests.pages.lamp.lamp_home_page import LampHomePage
from regression_tests.pages.lamp.lamp_tech_docs_page import LampTechDocsPage


def test_lamp_startup(context, base_url):
    # Verifies the app started and the LAMP Stack landing page is served by Apache.
    home_page = LampHomePage(context)
    home_page.navigate(base_url)
    expect(context, "LAMP Stack is not started: page title not found.").to_have_title(
        "LAMP Stack - Powered by Akamai Cloud Compute Marketplace"
    )
    expect(home_page.heading, "LAMP Stack heading did not render.").to_be_visible()
    expect(home_page.what_is_lamp_heading, "What is LAMP? heading did not render.").to_be_visible()


def test_lamp_tech_docs(context, techdocs_url):
    """Verify that the LAMP Stack tech docs page is accessible."""
    tech_docs_page = LampTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "LAMP Stack tech docs page did not load.").to_have_title("LAMP Stack")
    expect(tech_docs_page.lamp_header, "LAMP Stack tech docs header did not render.").to_be_visible()
