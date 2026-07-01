from playwright.sync_api import expect

from regression_tests.pages.jenkins.jenkins_unlock_page import JenkinsUnlockPage
from regression_tests.pages.jenkins.jenkins_setup_wizard_page import JenkinsSetupWizardPage
from regression_tests.pages.jenkins.jenkins_login_page import JenkinsLoginPage
from regression_tests.pages.jenkins.jenkins_dashboard_page import JenkinsDashboardPage
from regression_tests.pages.jenkins.jenkins_new_item_page import JenkinsNewItemPage
from regression_tests.pages.jenkins.jenkins_job_config_page import JenkinsJobConfigPage


def test_jenkins_startup(context, base_url):
    # Verifies the app started and the Unlock Jenkins setup wizard page loads.
    unlock_page = JenkinsUnlockPage(context)
    unlock_page.navigate(base_url)
    expect(context, "Jenkins did not start: page title not found.").to_have_title("Sign in - Jenkins")
    expect(unlock_page.heading, "Unlock Jenkins heading did not render.").to_be_visible()
    expect(unlock_page.admin_password_input, "Administrator password input did not render.").to_be_visible()


def test_jenkins_setup_wizard(context, base_url, app_credentials):
    # Completes the setup wizard: unlocks Jenkins, installs suggested plugins,
    # skips admin creation and instance config, then verifies the dashboard loads.
    password = app_credentials["Jenkins Admin password"]

    unlock_page = JenkinsUnlockPage(context)
    unlock_page.navigate(base_url)
    unlock_page.unlock(password)

    wizard_page = JenkinsSetupWizardPage(context)
    expect(wizard_page.install_suggested_button, "Customize Jenkins page did not appear after unlock.").to_be_visible()
    wizard_page.install_suggested_button.click()

    # Plugin installation can take several minutes on a fresh instance; 5 min covers slow CI runners.
    expect(wizard_page.skip_admin_button, "Plugin installation did not complete in time.").to_be_visible(timeout=300000)
    wizard_page.skip_admin_button.click()

    expect(wizard_page.save_and_finish_button, "Instance Configuration page did not appear.").to_be_visible()
    wizard_page.save_and_finish_button.click()

    expect(wizard_page.jenkins_ready_heading, "Jenkins is ready page did not appear.").to_be_visible()
    wizard_page.start_using_button.click()

    dashboard_page = JenkinsDashboardPage(context)
    expect(context, "Dashboard did not load after completing setup wizard.").to_have_title("Dashboard - Jenkins")
    expect(dashboard_page.welcome_heading, "Dashboard welcome heading not visible after setup.").to_be_visible()


def test_jenkins_dashboard_login(context, base_url, app_credentials):
    # Logs in as the existing admin user and creates a dummy Freestyle project job.
    password = app_credentials["Jenkins Admin password"]

    login_page = JenkinsLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Login page did not load.").to_have_title("Sign in - Jenkins")
    login_page.login("admin", password)

    dashboard_page = JenkinsDashboardPage(context)
    expect(context, "Dashboard did not load after login.").to_have_title("Dashboard - Jenkins")
    expect(dashboard_page.welcome_heading, "Dashboard welcome heading not visible after login.").to_be_visible()

    dashboard_page.new_item_link.click()

    new_item_page = JenkinsNewItemPage(context)
    expect(context, "New Item page did not load.").to_have_title("New Item - Jenkins")
    new_item_page.item_name_input.fill("dummy-test-job")
    new_item_page.freestyle_option.click()
    new_item_page.ok_button.click()

    job_config_page = JenkinsJobConfigPage(context)
    job_config_page.save_button.click()
    expect(context, "Job was not created: job page did not load.").to_have_title("dummy-test-job - Jenkins")
