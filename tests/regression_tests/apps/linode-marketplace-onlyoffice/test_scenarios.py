from playwright.sync_api import expect
from regression_tests.pages.onlyoffice.onlyoffice_tech_docs_page import OnlyofficeTechDocsPage


def test_onlyoffice_tech_docs(context, techdocs_url):
    """Verify that the ONLYOFFICE tech docs page is accessible."""
    tech_docs_page = OnlyofficeTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "ONLYOFFICE tech docs title did not match.").to_have_title("ONLYOFFICE Docs")
    expect(tech_docs_page.onlyoffice_header, "ONLYOFFICE tech docs header did not render.").to_be_visible()
