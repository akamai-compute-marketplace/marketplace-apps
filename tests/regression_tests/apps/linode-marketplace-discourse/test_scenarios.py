from uuid import uuid4

from playwright.sync_api import expect

from regression_tests.pages.discourse.discourse_home_page import DiscourseHomePage
from regression_tests.pages.discourse.discourse_login_page import DiscourseLoginPage
from regression_tests.pages.discourse.discourse_tech_docs_page import DiscourseTechDocsPage


def test_discourse_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    home_page = DiscourseHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Discourse is not started").to_have_title("Discourse")
    expect(home_page.log_in_button, "Login button did not render.").to_be_visible()


def test_discourse_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Discourse Admin username"]
    password = app_credentials["Discourse Admin Password"]
    home_page = DiscourseHomePage(context)
    home_page.navigate(base_url)
    home_page.open_login_page()
    login_page = DiscourseLoginPage(context)
    login_page.login(username, password)
    expect(home_page.new_topic_button, "Credentials are invalid or something went wrong.").to_be_visible()


def test_discourse_create_topic(context, base_url, app_credentials):
    # Verifies that an admin can create a topic and see it in the topic list.
    username = app_credentials["Discourse Admin username"]
    password = app_credentials["Discourse Admin Password"]
    topic_title = f"playwright-regression-test-{uuid4().hex[:8]}"
    topic_content = "This automated test verifies that a new forum topic can be created successfully."
    home_page = DiscourseHomePage(context)
    home_page.navigate(base_url)
    home_page.open_login_page()
    login_page = DiscourseLoginPage(context)
    login_page.login(username, password)
    home_page.create_new_topic(topic_title, topic_content)
    home_page.navigate(base_url)
    home_page.reload()
    expect(home_page.get_topic_link(topic_title), "Created topic did not appear in the topic list.").to_be_visible()


def test_discourse_tech_docs(context, techdocs_url):
    """Verify that the Discourse tech docs page is accessible."""
    tech_docs_page = DiscourseTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Discourse tech docs page did not load.").to_have_title("Discourse")
    expect(tech_docs_page.discourse_header, "Discourse tech docs header did not render.").to_be_visible()
