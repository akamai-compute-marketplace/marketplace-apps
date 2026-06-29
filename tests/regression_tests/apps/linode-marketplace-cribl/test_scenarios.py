import time

from playwright.sync_api import expect

from regression_tests.pages.cribl.cribl_login_page import CriblLoginPage
from regression_tests.pages.cribl.cribl_registration_page import CriblRegistrationPage
from regression_tests.pages.cribl.cribl_pipelines_page import CriblPipelinesPage


def test_cribl_startup(context, base_url):
    # Verifies that Cribl started and the login page loads successfully.
    login_page = CriblLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Cribl is not started — login page title mismatch.").to_have_title(
        "Login | Cribl"
    )
    expect(login_page.username_input, "Login form did not render on the screen.").to_be_visible()


def test_cribl_login(context, base_url, app_credentials):
    # Verifies admin login and completes the one-time Product Registration dialog.
    username = app_credentials["Cribl Admin User"]
    password = app_credentials["Cribl Admin Password"]
    email = "admin@example.com"

    login_page = CriblLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    registration_page = CriblRegistrationPage(context)
    registration_page.register(email)

    expect(context, "Cribl Stream dashboard did not load after registration.").to_have_title(
        "Cribl Stream", timeout=30000
    )


def test_cribl_create_pipeline(context, base_url, app_credentials):
    # Verifies that a new pipeline can be created and appears in the pipelines list.
    username = app_credentials["Cribl Admin User"]
    password = app_credentials["Cribl Admin Password"]

    login_page = CriblLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    expect(context, "Cribl Stream dashboard did not load after login.").to_have_title(
        "Cribl Stream", timeout=30000
    )

    pipelines_page = CriblPipelinesPage(context)
    pipelines_page.navigate_to_pipelines(base_url)

    pipeline_name = f"test_pipeline_{int(time.time())}"
    pipelines_page.create_pipeline(pipeline_name)

    pipelines_page.navigate_to_pipelines(base_url)
    expect(
        pipelines_page.pipeline_link(pipeline_name),
        f"Newly created pipeline '{pipeline_name}' did not appear in the pipelines list.",
    ).to_be_visible(timeout=15000)
