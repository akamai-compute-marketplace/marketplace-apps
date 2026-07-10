from playwright.sync_api import expect

from regression_tests.pages.hashicorp_vault.vault_dashboard_page import VaultDashboardPage
from regression_tests.pages.hashicorp_vault.vault_login_page import VaultLoginPage
from regression_tests.pages.hashicorp_vault.vault_secrets_page import VaultSecretsPage


def test_vault_startup(context, base_url):
    # Verifies that the HashiCorp Vault is started
    login_page = VaultLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Vault is not started").to_have_title("Vault")
    expect(login_page.sign_in_button, "The sign in button did not render on the screen.").to_be_visible()


def test_vault_initial_token(context, base_url, app_credentials):
    # Verifies that user can log in with initial root token
    login_secret = app_credentials["Initial Root Token"]
    login_page = VaultLoginPage(context)
    login_page.navigate(base_url)
    expect(login_page.sign_in_button, "The sign in button did not render on the screen.").to_be_visible()
    login_page.sign_in(login_secret)
    dashboard_page = VaultDashboardPage(context)
    expect(dashboard_page.secrets_engines_link, "Can not log in with initial root token").to_be_visible()


def test_vault_create_secret(context, base_url, app_credentials):
    # Verifies that secret can be created
    login_secret = app_credentials["Initial Root Token"]
    engine_name = "vault-test-engine"
    test_secret_path = "test-secret-path"
    test_secret_key = "test-secret-key"
    test_secret_value = "test-secret-value"
    login_page = VaultLoginPage(context)
    login_page.navigate(base_url)
    expect(login_page.sign_in_button, "The sign in button did not render on the screen.").to_be_visible()
    login_page.sign_in(login_secret)
    dashboard_page = VaultDashboardPage(context)
    expect(dashboard_page.secrets_engines_link, "Can not log in with initial root token").to_be_visible()
    dashboard_page.open_secrets_engines()
    secrets_page = VaultSecretsPage(context)
    secrets_page.create_new_engine(engine_name)
    secrets_page.create_new_secret(secret_path=test_secret_path, secret_key=test_secret_key, secret_value=test_secret_value)
    secrets_page.get_secret_data()
    expect(secrets_page.secret_data_row, "The secret key is not visible on the screen or incorrect").to_contain_text(test_secret_key)
    expect(secrets_page.secret_data_row, "The secret value is not visible on the screen or incorrect").to_contain_text(test_secret_value)
