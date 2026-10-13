from playwright.sync_api import expect

from regression_tests.pages.backstage.backstage_landing_page import BackstageLandingPage
from regression_tests.pages.backstage.backstage_tech_docs_page import BackstageTechDocsPage


def test_backstage_startup(context, base_url):
    # Verifies that the Backstage app has started and the landing page loads successfully.
    landing_page = BackstageLandingPage(context)
    landing_page.navigate(base_url)
    expect(context, "Backstage is not started").to_have_title("Scaffolded Backstage App | Scaffolded Backstage App")
    expect(landing_page.app_heading, "Backstage main heading did not render.").to_be_visible()
    expect(landing_page.guest_enter_button, "Backstage guest sign-in button did not render.").to_be_visible()


def test_backstage_tech_docs(context, techdocs_url):
    """Verify that the Backstage tech docs page is accessible."""
    tech_docs_page = BackstageTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Backstage tech docs page did not load.").to_have_title("Backstage")
    expect(tech_docs_page.backstage_header, "Backstage tech docs header did not render.").to_be_visible()
