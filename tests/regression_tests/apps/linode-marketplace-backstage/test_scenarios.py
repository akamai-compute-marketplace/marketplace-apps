from playwright.sync_api import expect

from regression_tests.pages.backstage.backstage_landing_page import BackstageLandingPage


def test_backstage_startup(context, base_url):
    # Verifies that the Backstage app has started and the landing page loads successfully.
    landing_page = BackstageLandingPage(context)
    landing_page.navigate(base_url)
    expect(context, "Backstage is not started").to_have_title("Scaffolded Backstage App | Scaffolded Backstage App")
    expect(landing_page.app_heading, "Backstage main heading did not render.").to_be_visible()
    expect(landing_page.guest_enter_button, "Backstage guest sign-in button did not render.").to_be_visible()

