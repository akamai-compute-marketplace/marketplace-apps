from playwright.sync_api import expect
from regression_tests.pages.passbolt.passbolt_login_page import PassboltLoginPage
from regression_tests.pages.passbolt.passbolt_tech_docs_page import PassboltTechDocsPage


def test_passbolt_startup(context, base_url):
    # Verifies that Passbolt started and the login page loads successfully.
    login_page = PassboltLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Passbolt is not started").to_have_title(
        "Passbolt | Open source password manager for teams"
    )
    expect(login_page.username_input, "Login email field did not render.").to_be_visible(timeout=30000)


def test_passbolt_tech_docs(context, techdocs_url):
    """Verify that the Passbolt tech docs page is accessible."""
    tech_docs_page = PassboltTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Passbolt tech docs page title is incorrect.").to_have_title("Passbolt Community Edition")
    expect(tech_docs_page.passbolt_header, "Passbolt tech docs header did not render.").to_be_visible()
