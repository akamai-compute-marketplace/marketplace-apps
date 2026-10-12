import re

from playwright.sync_api import expect

from regression_tests.pages.gitlab.gitlab_login_page import GitLabLoginPage
from regression_tests.pages.gitlab.gitlab_setup_page import GitLabSetupPage
from regression_tests.pages.gitlab.gitlab_home_page import GitLabHomePage
from regression_tests.pages.gitlab.gitlab_new_project_page import GitLabNewProjectPage
from regression_tests.pages.gitlab.gitlab_tech_docs_page import GitLabTechDocsPage


def test_gitlab_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = GitLabLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "GitLab is not started").to_have_title("Sign in · GitLab")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_gitlab_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Gitlab User"]
    password = app_credentials["Gitlab Password"]
    login_page = GitLabLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    setup_page = GitLabSetupPage(context)
    setup_page.skip_setup_if_present()
    home_page = GitLabHomePage(context)
    expect(home_page.create_new_button, "Navigation not available after login — login may have failed.").to_be_visible()


def test_gitlab_create_project(context, base_url, app_credentials):
    # Verifies that the admin can create a project and it appears in GitLab.
    username = app_credentials["Gitlab User"]
    password = app_credentials["Gitlab Password"]
    project = "test-automation-new-project"
    login_page = GitLabLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    setup_page = GitLabSetupPage(context)
    setup_page.skip_setup_if_present()
    new_project_page = GitLabNewProjectPage(context)
    new_project_page.navigate(f"{base_url}/projects/new")
    new_project_page.create_project(project)
    expect(context, "Project page did not load after creation.").to_have_title(re.compile(project))


def test_gitlab_tech_docs(context, techdocs_url):
    """Verify that the GitLab tech docs page is accessible."""
    tech_docs_page = GitLabTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "GitLab tech docs page did not load.").to_have_title("GitLab")
    expect(tech_docs_page.gitlab_header, "GitLab tech docs header did not render.").to_be_visible()
