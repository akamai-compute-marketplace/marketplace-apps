import re
import time

from playwright.sync_api import expect

from regression_tests.pages.plesk.plesk_login_page import PleskLoginPage
from regression_tests.pages.plesk.plesk_setup_wizard_page import PleskSetupWizardPage
from regression_tests.pages.plesk.plesk_domains_page import PleskDomainsPage


def test_plesk_startup(context, base_url):
    """Verifies that Plesk started and the login page loads successfully."""
    login_page = PleskLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Plesk login page did not load — app may not have started.").to_have_title(
        re.compile(r"Plesk Obsidian.*")
    )
    expect(login_page.username_input, "Username input was not visible on the Plesk login page.").to_be_visible()
    expect(login_page.password_input, "Password input was not visible on the Plesk login page.").to_be_visible()


def test_plesk_login_and_setup_wizard(context, base_url, plesk_initial_login, plesk_admin_login):
    """Verifies that the root user can log in and complete the setup wizard using the free trial license."""
    login_page = PleskLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(plesk_initial_login["username"], plesk_initial_login["password"])

    wizard_page = PleskSetupWizardPage(context)
    expect(wizard_page.email_input, "Setup wizard did not load after login — login may have failed.").to_be_visible(
        timeout=30000
    )

    wizard_page.complete_setup_with_trial_license(
        email="admin@example.com",
        new_admin_password=plesk_admin_login["password"],
    )

    domains_page = PleskDomainsPage(context)
    expect(
        domains_page.websites_domains_heading,
        "Websites & Domains dashboard did not load — setup wizard may not have completed.",
    ).to_be_visible(timeout=60000)


def test_plesk_create_domain_and_check_active(context, base_url, plesk_admin_login):
    """Verifies that the admin user can create a domain with a blank website and it shows Active."""
    login_page = PleskLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(plesk_admin_login["username"], plesk_admin_login["password"])

    domains_page = PleskDomainsPage(context)
    expect(
        domains_page.websites_domains_heading,
        "Websites & Domains dashboard did not load — admin login may have failed.",
    ).to_be_visible(timeout=30000)

    # Use a unique domain per run so the test is safe to re-run on the same VM.
    unique_domain = f"regtest-{int(time.time())}.example.com"
    domains_page.create_blank_website_domain(unique_domain)

    expect(
        domains_page.domain_heading(unique_domain),
        "Domain overview page did not load — domain may not have been created.",
    ).to_be_visible(timeout=30000)
    expect(
        domains_page.domain_status,
        "Newly created domain does not show an Active status.",
    ).to_be_visible(timeout=30000)

