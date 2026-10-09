from playwright.sync_api import expect
from regression_tests.pages.plex.plex_sign_in_page import PlexSignInPage
from regression_tests.pages.plex.plex_tech_docs_page import PlexTechDocsPage


def test_plex_startup(context, base_url):
    """Verifies that Plex started and redirects to the Plex.tv sign-in flow."""
    context.goto(base_url)
    expect(context, "Plex did not load — app may not have started.").to_have_title("Plex")
    sign_in_page = PlexSignInPage(context)
    expect(sign_in_page.continue_with_email_button, "Plex.tv sign-in options did not render.").to_be_visible(timeout=30000)


def test_plex_tech_docs(context, techdocs_url):
    """Verify that the Plex tech docs page is accessible."""
    tech_docs_page = PlexTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Plex tech docs page title is incorrect.").to_have_title("Plex Media Server")
    expect(tech_docs_page.plex_header, "Plex tech docs header did not render.").to_be_visible()
