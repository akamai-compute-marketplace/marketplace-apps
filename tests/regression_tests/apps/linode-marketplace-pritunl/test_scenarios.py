import re
import time

from playwright.sync_api import expect

from regression_tests.pages.pritunl.pritunl_login_page import PritunlLoginPage
from regression_tests.pages.pritunl.pritunl_setup_wizard_page import PritunlSetupWizardPage
from regression_tests.pages.pritunl.pritunl_organizations_page import PritunlOrganizationsPage
from regression_tests.pages.pritunl.pritunl_servers_page import PritunlServersPage


def test_pritunl_startup(context, base_url):
    """Verifies that Pritunl started and the login page loads successfully."""
    login_page = PritunlLoginPage(context)
    login_page.navigate(f"{base_url}/login")
    expect(context, "Pritunl login page did not load — app may not have started.").to_have_title("Pritunl")
    expect(login_page.username_input, "Username input was not visible on the Pritunl login page.").to_be_visible()
    expect(login_page.password_input, "Password input was not visible on the Pritunl login page.").to_be_visible()


def test_pritunl_login_and_setup_wizard(context, base_url, app_credentials):
    """Verifies that the admin user can log in and complete the Initial Setup wizard."""
    username = app_credentials["Pritunl Username"]
    password = app_credentials["Pritunl Password"]

    login_page = PritunlLoginPage(context)
    login_page.navigate(f"{base_url}/login")
    login_page.login(username, password)

    wizard_page = PritunlSetupWizardPage(context)
    expect(
        wizard_page.modal_title, "Initial Setup wizard did not appear after login — login may have failed."
    ).to_have_text("Initial Setup", timeout=30000)

    wizard_page.complete_setup()
    expect(
        wizard_page.success_alert, "Initial Setup wizard did not confirm a successful save."
    ).to_be_visible(timeout=30000)


def test_pritunl_create_server_and_verify_online(context, base_url, app_credentials):
    """Verifies that an org and server can be created, attached, started, and shown online on the dashboard."""
    username = app_credentials["Pritunl Username"]
    password = app_credentials["Pritunl Password"]

    login_page = PritunlLoginPage(context)
    login_page.navigate(f"{base_url}/login")
    login_page.login(username, password)

    wizard_page = PritunlSetupWizardPage(context)
    expect(
        wizard_page.modal_title, "Initial Setup wizard did not appear after login — login may have failed."
    ).to_have_text("Initial Setup", timeout=30000)
    wizard_page.complete_setup()
    expect(
        wizard_page.success_alert, "Initial Setup wizard did not confirm a successful save."
    ).to_be_visible(timeout=30000)

    # Use a unique name per run so the test is safe to re-run on the same VM.
    unique_suffix = int(time.time())
    org_name = f"regtest-org-{unique_suffix}"
    server_name = f"regtest-server-{unique_suffix}"

    orgs_page = PritunlOrganizationsPage(context)
    orgs_page.navigate(f"{base_url}/#users")
    orgs_page.create_organization(org_name)
    expect(orgs_page.success_alert, "Organization was not created successfully.").to_be_visible(timeout=30000)

    servers_page = PritunlServersPage(context)
    servers_page.navigate(f"{base_url}/#servers")
    servers_page.create_server(server_name)

    servers_page.attach_organization(org_name, server_name)
    expect(
        servers_page.start_server_button(server_name),
        "Start Server button was not enabled after attaching organization.",
    ).to_be_enabled(timeout=30000)

    servers_page.start_server(server_name)
    expect(
        servers_page.server_status(server_name), "Server status is not Online."
    ).to_contain_text("Online", timeout=30000)

    servers_page.navigate(f"{base_url}/#dashboard")
    expect(
        servers_page.dashboard_servers_status, "Dashboard servers status never loaded past its placeholder."
    ).to_contain_text(re.compile(r"\d+/\d+"), timeout=30000)
    status_text = servers_page.dashboard_servers_status.inner_text()
    match = re.search(r"(\d+)/(\d+)", status_text)
    assert match, f"Could not parse the dashboard's servers-online status: {status_text!r}"
    online, total = match.groups()
    assert online == total and online != "0", f"Dashboard does not show all servers online: {status_text!r}"
