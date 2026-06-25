from playwright.sync_api import expect

from regression_tests.pages.drupal.drupal_create_article_page import DrupalCreateArticlePage
from regression_tests.pages.drupal.drupal_home_page import DrupalHomePage
from regression_tests.pages.drupal.drupal_login_page import DrupalLoginPage


def test_drupal_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = DrupalLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    expect(context, "Drupal is not started").to_have_title("Log in | My Drupal Site")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_drupal_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Drupal Admin Username"]
    password = app_credentials["Drupal Admin Password"]
    login_page = DrupalLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    login_page.login(username, password)
    home_page = DrupalHomePage(context)
    home_page.navigate(base_url)
    expect(home_page.logout_link, "Credentials are invalid or something went wrong.").to_be_visible()


def test_drupal_create_article(context, base_url, app_credentials):
    # Verifies that an admin can create an Article and see it published on the home page.
    username = app_credentials["Drupal Admin Username"]
    password = app_credentials["Drupal Admin Password"]
    article_title = "Test Article Title"
    article_body = "Test Automation Article Body"

    login_page = DrupalLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    login_page.login(username, password)

    create_article_page = DrupalCreateArticlePage(context)
    create_article_page.navigate(f"{base_url}/node/add/article")
    create_article_page.create_article(article_title, article_body)

    home_page = DrupalHomePage(context, article_title=article_title, article_body=article_body)
    home_page.navigate(base_url)
    expect(home_page.article_heading, "Failed to create a new article.").to_be_visible()
    expect(home_page.article_body, "Article body is not displayed on the home page.").to_be_visible()
