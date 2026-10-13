from playwright.sync_api import expect

from regression_tests.pages.cloudron.cloudron_setup_page import CloudronSetupPage
from regression_tests.pages.cloudron.cloudron_tech_docs_page import CloudronTechDocsPage


def test_cloudron_startup(context, base_url):
    # Verifies that Cloudron started and the initial domain setup wizard is shown.
    setup_page = CloudronSetupPage(context)
    setup_page.navigate(base_url)
    expect(context, "Cloudron is not started").to_have_title("Domain Setup")
    expect(setup_page.heading, "Domain Setup wizard did not render.").to_be_visible()
    expect(setup_page.domain_input, "Domain input field did not render.").to_be_visible()


def test_cloudron_tech_docs(context, techdocs_url):
    """Verify that the Cloudron tech docs page is accessible."""
    tech_docs_page = CloudronTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Cloudron tech docs page did not load.").to_have_title("Cloudron")
    expect(tech_docs_page.cloudron_header, "Cloudron tech docs header did not render.").to_be_visible()
