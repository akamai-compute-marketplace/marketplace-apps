from uuid import uuid4

import pytest
from playwright.sync_api import expect

from regression_tests.pages.coolify.coolify_dashboard_page import CoolifyDashboardPage
from regression_tests.pages.coolify.coolify_database_page import CoolifyDatabasePage
from regression_tests.pages.coolify.coolify_environment_page import CoolifyEnvironmentPage
from regression_tests.pages.coolify.coolify_login_page import CoolifyLoginPage
from regression_tests.pages.coolify.coolify_tech_docs_page import CoolifyTechDocsPage


def test_coolify_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = CoolifyLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Coolify is not started").to_have_title("Coolify")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_coolify_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Admin Email"]
    password = app_credentials["Admin Password"]
    login_page = CoolifyLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    login_page.skip_setup_if_present()
    dashboard_page = CoolifyDashboardPage(context)
    expect(context, "Dashboard did not load after login.").to_have_title("Dashboard | Coolify")
    expect(dashboard_page.projects_nav_link, "Credentials are invalid or something went wrong.").to_be_visible()


def test_coolify_create_project_with_sqlite(context, base_url, app_credentials):
    # Verifies that an admin can create a project, add a SQLite database to it, and the database becomes running and healthy.
    username = app_credentials["Admin Email"]
    password = app_credentials["Admin Password"]
    project_name = f"test-project-{uuid4().hex[:8]}"
    login_page = CoolifyLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = CoolifyDashboardPage(context)
    dashboard_page.create_project(project_name)
    environment_page = CoolifyEnvironmentPage(context)
    expect(environment_page.get_project_link(project_name), "Project was not created.").to_be_visible()
    environment_page.add_sqlite_database()
    database_page = CoolifyDatabasePage(context)
    expect(database_page.start_button, "SQLite database page did not load.").to_be_visible(timeout=30000)
    database_page.start()
    expect(database_page.startup_logs_finished_status, "SQLite database startup did not finish.").to_have_text(
        "Finished", timeout=180000
    )
    database_page.close_startup_logs()
    expect(database_page.running_status_button, "SQLite database is not running.").to_be_visible(timeout=60000)
    database_page.open_status_menu()
    expect(database_page.healthcheck_healthy_item, "SQLite database is not healthy.").to_be_visible(timeout=60000)


@pytest.mark.xfail(reason="Tech docs page is not ready yet")
def test_coolify_tech_docs(context, techdocs_url):
    """Verify that the Coolify tech docs page is accessible."""
    tech_docs_page = CoolifyTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Coolify tech docs page did not load.").to_have_title("Coolify")
    expect(tech_docs_page.coolify_header, "Coolify tech docs header did not render.").to_be_visible()
