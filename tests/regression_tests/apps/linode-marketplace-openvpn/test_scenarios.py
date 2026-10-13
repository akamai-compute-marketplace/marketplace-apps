from playwright.sync_api import expect
from regression_tests.pages.openvpn.openvpn_license_agreement_page import OpenVPNLicenseAgreementPage
from regression_tests.pages.openvpn.openvpn_login_page import OpenVPNLoginPage
from regression_tests.pages.openvpn.openvpn_status_page import OpenVPNStatusPage
from regression_tests.pages.openvpn.openvpn_tech_docs_page import OpenVPNTechDocsPage


def test_openvpn_startup(context, base_url):
    # Verifies that the app started and the admin login page loads successfully.
    login_page = OpenVPNLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "OpenVPN admin portal is not started").to_have_title("Access server admin portal")
    expect(login_page.username_input, "Login form did not render.").to_be_visible()


def test_openvpn_admin_login(context, base_url, app_credentials):
    # Verifies that the admin user can log in with the provided credentials. On a fresh instance
    # this also has to get past the one-time License Agreement dialog before the dashboard loads.
    username = app_credentials["OpenVPN Username"]
    password = app_credentials["OpenVPN Password"]
    login_page = OpenVPNLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)

    license_agreement_page = OpenVPNLicenseAgreementPage(context)
    license_agreement_page.accept_if_present()

    status_page = OpenVPNStatusPage(context)
    expect(status_page.heading, "Credentials are invalid or something went wrong.").to_be_visible()


def test_openvpn_tech_docs(context, techdocs_url):
    """Verify that the OpenVPN tech docs page is accessible."""
    tech_docs_page = OpenVPNTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "OpenVPN tech docs title did not match.").to_have_title("OpenVPN")
    expect(tech_docs_page.openvpn_header, "OpenVPN tech docs header did not render.").to_be_visible()
