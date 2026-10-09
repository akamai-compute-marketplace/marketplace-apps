import pytest
from playwright.sync_api import expect

from regression_tests.pages.openfang.openfang_tech_docs_page import OpenFangTechDocsPage


@pytest.mark.xfail(reason="Tech docs page is not ready yet")
def test_openfang_tech_docs(context, techdocs_url):
    """Verify that the OpenFang tech docs page is accessible."""
    tech_docs_page = OpenFangTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenFang tech docs title did not match.").to_have_title("OpenFang")
    expect(tech_docs_page.openfang_header, "OpenFang tech docs header did not render.").to_be_visible()
