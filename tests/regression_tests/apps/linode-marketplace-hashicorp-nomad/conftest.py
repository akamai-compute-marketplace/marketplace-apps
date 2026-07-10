from pathlib import Path

import pytest


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides NGINX Basic Auth credentials for the HashiCorp Nomad browser context.
    Overrides the default (None) from the global conftest.
    """
    return {
        "username": app_credentials["NGINX Basic Auth Username"],
        "password": app_credentials["NGINX Basic Auth Password"],
    }


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote HashiCorp Nomad.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "../home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base URL for the HashiCorp Nomad.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the HashiCorp Nomad.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def job_definition() -> str:
    return (Path(__file__).parent / "job_definition.txt").read_text()