from playwright.sync_api import expect

from regression_tests.pages.gitea.gitea_create_repo_page import GiteaCreateRepoPage
from regression_tests.pages.gitea.gitea_dashboard_page import GiteaDashboardPage
from regression_tests.pages.gitea.gitea_login_page import GiteaLoginPage
from regression_tests.pages.gitea.gitea_repo_page import GiteaRepoPage


def test_gitea_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = GiteaLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    expect(context, "Gitea is not started").to_have_title("Sign In - Gitea")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_gitea_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = app_credentials["Gitea Admin User"]
    password = app_credentials["Gitea Admin Password"]
    login_page = GiteaLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    login_page.login(username, password)
    dashboard_page = GiteaDashboardPage(context)
    expect(dashboard_page.new_repository_link, "Credentials are invalid or something went wrong.").to_be_visible()


def test_gitea_create_repo(context, base_url, app_credentials):
    # Verifies that the admin can create a repository and see it after creation.
    username = app_credentials["Gitea Admin User"]
    password = app_credentials["Gitea Admin Password"]
    repo_name = "test-automation-repo"

    login_page = GiteaLoginPage(context)
    login_page.navigate(f"{base_url}/user/login")
    login_page.login(username, password)

    create_repo_page = GiteaCreateRepoPage(context)
    create_repo_page.navigate(f"{base_url}/repo/create")
    create_repo_page.create_repo(repo_name)

    repo_page = GiteaRepoPage(context, repo_name)
    expect(repo_page.repo_name_link, "Failed to create the repository.").to_be_visible()
