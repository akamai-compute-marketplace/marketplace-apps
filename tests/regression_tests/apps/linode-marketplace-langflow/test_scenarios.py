from playwright.sync_api import expect

from regression_tests.pages.langflow.langflow_login_page import LangflowLoginPage
from regression_tests.pages.langflow.langflow_flows_page import LangflowFlowsPage


def test_langflow_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = LangflowLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Langflow is not started").to_have_title("Langflow")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_langflow_login(context, base_url, app_credentials):
    # Verifies that the user can log in with provided credentials.
    username = app_credentials["Langflow Admin Username"]
    password = app_credentials["Langflow Admin Password"]
    login_page = LangflowLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    flows_page = LangflowFlowsPage(context)
    expect(flows_page.user_menu_button, "App shell did not load after login.").to_be_visible(timeout=30000)
