from playwright.sync_api import expect

from regression_tests.pages.peppermint.peppermint_create_issue_page import PeppermintCreateIssuePage
from regression_tests.pages.peppermint.peppermint_dashboard_page import PeppermintDashboardPage
from regression_tests.pages.peppermint.peppermint_issues_page import PeppermintIssuesPage
from regression_tests.pages.peppermint.peppermint_login_page import PeppermintLoginPage
from regression_tests.pages.peppermint.peppermint_onboarding_page import PeppermintOnboardingPage


def test_peppermint_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = PeppermintLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Peppermint is not started").to_have_title("Peppermint")
    expect(login_page.email_input, "Login form did not render.").to_be_visible()


def test_peppermint_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials. On a fresh instance
    # this also has to get past the one-time onboarding welcome screen before the dashboard loads.
    email = app_credentials["Admin Email"]
    password = app_credentials["Admin Password"]
    login_page = PeppermintLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)

    onboarding_page = PeppermintOnboardingPage(context)
    onboarding_page.complete_if_present()

    dashboard_page = PeppermintDashboardPage(context)
    expect(dashboard_page.account_menu_button, "Credentials are invalid or something went wrong.").to_be_visible(
        timeout=30000
    )


def test_peppermint_create_issue(context, base_url, app_credentials):
    # Verifies that an admin can create an Issue and see it listed on the Issues page.
    email = app_credentials["Admin Email"]
    password = app_credentials["Admin Password"]
    issue_title = "Test Automation Issue"

    login_page = PeppermintLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(email, password)

    onboarding_page = PeppermintOnboardingPage(context)
    onboarding_page.complete_if_present()

    dashboard_page = PeppermintDashboardPage(context)
    expect(dashboard_page.account_menu_button, "Credentials are invalid or something went wrong.").to_be_visible(
        timeout=30000
    )
    dashboard_page.open_new_issue_dialog()

    create_issue_page = PeppermintCreateIssuePage(context)
    create_issue_page.create_issue(
        title=issue_title,
        name="Test Automation",
        email="test-automation@example.com",
        description="Automated regression test issue body.",
    )

    issues_page = PeppermintIssuesPage(context)
    expect(
        issues_page.issue_link(issue_title), "Failed to create a new issue."
    ).to_be_visible()
