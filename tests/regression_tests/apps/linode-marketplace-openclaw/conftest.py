import time

import pytest

from regression_tests.utils.ssh import ssh_connection


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote OpenClaw server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "../home/admin/.credentials"


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides Basic Auth credentials for the Openclaw browser context.
    Overrides the default (None) from the global conftest.
    """
    return {
        "username": app_credentials["Htpasswd username"],
        "password": app_credentials["Htpassword"],
    }


@pytest.fixture(scope="session")
def openclaw_onboarding(ssh_credentials):
    """
    Runs the OpenClaw onboarding as the ``openclaw`` system user via SSH.

    Executes:
      1. ``openclaw onboard --non-interactive --accept-risk --install-daemon``
      2. ``openclaw dashboard``

    Args:
        ssh_credentials: A (host, username, password) tuple from the global conftest.

    """
    host, username, password = ssh_credentials

    with ssh_connection(host, username, password) as client:
        client.exec_command("su - openclaw -c 'openclaw onboard --non-interactive --accept-risk --install-daemon'")
        time.sleep(120)  # Wait for onboarding to complete before starting the dashboard
        client.exec_command("su - openclaw -c 'openclaw dashboard'")
        time.sleep(60)  # Wait for the dashboard to start before proceeding with tests


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base URL for the OpenClaw dashboard.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the OpenClaw dashboard.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"
