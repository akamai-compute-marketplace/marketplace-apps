import pytest
from playwright.sync_api import expect

from regression_tests.pages.opencode.opencode_tech_docs_page import OpenCodeTechDocsPage


@pytest.mark.xfail(reason="Tech docs page is not ready yet")
def test_opencode_tech_docs(context, techdocs_url):
    """Verify that the OpenCode tech docs page is accessible."""
    tech_docs_page = OpenCodeTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenCode tech docs title did not match.").to_have_title("OpenCode")
    expect(tech_docs_page.opencode_header, "OpenCode tech docs header did not render.").to_be_visible()
