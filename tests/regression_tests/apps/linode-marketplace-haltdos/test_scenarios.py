from playwright.sync_api import expect

from regression_tests.pages.haltdos.haltdos_login_page import HaltdosLoginPage
from regression_tests.pages.haltdos.haltdos_tech_docs_page import HaltdosTechDocsPage


def test_haltdos_login(context, base_url):
    # Verifies that the Haltdos is started and user can log in with basic auth credentials
    login_page = HaltdosLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Haltdos is not started").to_have_title("Haltdos Management Console")
    expect(login_page.full_name_field, "Can not log in with basic auth credentials").to_be_visible()


def test_haltdos_tech_docs(context, techdocs_url):
    """Verify that the Haltdos Community WAF tech docs page is accessible."""
    tech_docs_page = HaltdosTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Haltdos Community WAF tech docs page did not load.").to_have_title("Haltdos Community WAF")
    expect(tech_docs_page.haltdos_header, "Haltdos Community WAF tech docs header did not render.").to_be_visible()
