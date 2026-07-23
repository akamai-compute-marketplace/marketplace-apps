from playwright.sync_api import expect

from regression_tests.pages.rabbitmq.rabbitmq_login_page import RabbitMQLoginPage
from regression_tests.pages.rabbitmq.rabbitmq_overview_page import RabbitMQOverviewPage


def test_rabbitmq_startup(context, base_url):
    """Verifies that RabbitMQ started and the management login page loads successfully."""
    login_page = RabbitMQLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "RabbitMQ management login page did not load.").to_have_title("RabbitMQ Management")
    expect(login_page.username_input, "RabbitMQ login form did not render.").to_be_visible()
    expect(login_page.password_input, "RabbitMQ login form did not render.").to_be_visible()


def test_rabbitmq_login(context, base_url, app_credentials):
    """Verifies that the admin user can log in to the RabbitMQ management UI."""
    username = app_credentials["RabbitMQ Admin Username"]
    password = app_credentials["RabbitMQ Admin Password"]
    login_page = RabbitMQLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    overview_page = RabbitMQOverviewPage(context)
    expect(context, "RabbitMQ overview page did not load after login.").to_have_title("RabbitMQ: Overview")
    expect(overview_page.overview_heading, "Overview heading not visible after login.").to_be_visible()
    expect(overview_page.logout_button, "Log out button not visible after login.").to_be_visible()
