from playwright.sync_api import expect

from regression_tests.pages.mastodon.mastodon_landing_page import MastodonLandingPage
from regression_tests.pages.mastodon.mastodon_login_page import MastodonLoginPage
from regression_tests.pages.mastodon.mastodon_home_page import MastodonHomePage


def test_mastodon_startup(context, base_url):
    # Verifies the app started and the Mastodon public explore page loads.
    landing_page = MastodonLandingPage(context)
    landing_page.navigate(base_url)
    expect(context, "Mastodon is not started: page title not found.").to_have_title("Trending - Mastodon")
    expect(landing_page.login_link, "Login link did not render on the landing page.").to_be_visible()
    expect(landing_page.trending_heading, "Trending heading did not render.").to_be_visible()


def test_mastodon_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    email = app_credentials["Owner Email"]
    password = app_credentials["Owner Password"]
    login_page = MastodonLoginPage(context)
    login_page.navigate(f"{base_url}/auth/sign_in")
    login_page.login(email, password)
    home_page = MastodonHomePage(context)
    expect(home_page.compose_input, "Compose box not visible — login may have failed.").to_be_visible()


def test_mastodon_write_post(context, base_url, app_credentials):
    # Verifies that the admin user can write a post and it appears on the home feed.
    email = app_credentials["Owner Email"]
    password = app_credentials["Owner Password"]
    login_page = MastodonLoginPage(context)
    login_page.navigate(f"{base_url}/auth/sign_in")
    login_page.login(email, password)
    home_page = MastodonHomePage(context)
    home_page.navigate(f"{base_url}/home")
    post_text = "Hello from the regression test suite!"
    home_page.write_post(post_text)
    expect(home_page.home_feed, "Post did not appear in the home feed after posting.").to_contain_text(post_text)
