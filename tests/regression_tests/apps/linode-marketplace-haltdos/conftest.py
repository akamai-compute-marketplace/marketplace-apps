from pathlib import Path

import pytest


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides NGINX Basic Auth credentials for the Haltdos browser context.
    Overrides the default (None) from the global conftest.
    """
    return {
        "username": app_credentials["NGINX Setup-Wizard Auth Username"],
        "password": app_credentials["NGINX Setup-Wizard Auth Password"],
    }


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Haltdos.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "../home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base URL for the Haltdos.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the Haltdos.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:9000/setup"
