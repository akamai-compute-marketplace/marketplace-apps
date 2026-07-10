from playwright.sync_api import expect

from regression_tests.pages.joomla.joomla_admin_login_page import JoomlaAdminLoginPage
from regression_tests.pages.joomla.joomla_articles_page import JoomlaArticlesPage
from regression_tests.pages.joomla.joomla_create_article_page import JoomlaCreateArticlePage
from regression_tests.pages.joomla.joomla_create_menu_item_page import JoomlaCreateMenuItemPage
from regression_tests.pages.joomla.joomla_dashboard_page import JoomlaDashboardPage
from regression_tests.pages.joomla.joomla_home_article_page import JoomlaHomeArticlePage
from regression_tests.pages.joomla.joomla_home_page import JoomlaHomePage
from regression_tests.pages.joomla.joomla_menu_items_page import JoomlaMenuItemsPage


def test_joomla_startup(context, admin_url):
    # Verifies that the Joomla started and login page loads successfully.
    login_page = JoomlaAdminLoginPage(context)
    login_page.navigate(admin_url)
    expect(context, "Joomla is not started").to_have_title("Joomla on Linode - Administration")
    expect(login_page.username_input, "The username input field did not render on the screen.").to_be_visible()


def test_joomla_login(context, admin_url, app_credentials):
    # Verifies that user can loging to Joomla with provided credentials.
    username = app_credentials["Joomla Admin Username"]
    password = app_credentials["Joomla Admin Password"]
    login_page = JoomlaAdminLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(username, password)
    dashboard_page = JoomlaDashboardPage(context)
    dashboard_page.dismiss_guided_tour()
    expect(dashboard_page.content_link, "Credentials are invalid or something went wrong").to_be_visible()


def test_joomla_publish_article(context, base_url, admin_url, app_credentials):
    # Verifies that user can create a new article in Joomla.
    username = app_credentials["Joomla Admin Username"]
    password = app_credentials["Joomla Admin Password"]
    article_title = "Test Article Title"
    article_text = "Test Automation Article Text"
    menu_item_title = "Test Menu Item Title"
    login_page = JoomlaAdminLoginPage(context)
    login_page.navigate(admin_url)
    login_page.login(username, password)

    dashboard_page = JoomlaDashboardPage(context)
    dashboard_page.create_article()
    create_article_page = JoomlaCreateArticlePage(context)
    create_article_page.complete_article_and_save(article_title, article_text)
    articles_page = JoomlaArticlesPage(context, article_title)
    expect(articles_page.article_title_link, "Failed to create a new article.").to_be_visible()

    dashboard_page.create_menu_item()
    create_menu_item_page = JoomlaCreateMenuItemPage(context, article_title, menu_item_title)
    create_menu_item_page.complete_menu_item_and_save()
    menu_items_page = JoomlaMenuItemsPage(context, menu_item_title)
    expect(menu_items_page.menu_item_title, "Failed to create a new menu item.").to_be_visible()

    home_page = JoomlaHomePage(context, menu_item_title)
    home_page.navigate(base_url)
    expect(home_page.article_link, "Failed to publish a new article.").to_be_visible()
    home_page.open_article_link()
    home_article_page = JoomlaHomeArticlePage(context)
    expect(home_article_page.article_title, "Article title is incorrect").to_have_text(article_title)
    expect(home_article_page.article_text, "Article text is incorrect").to_have_text(article_text)
