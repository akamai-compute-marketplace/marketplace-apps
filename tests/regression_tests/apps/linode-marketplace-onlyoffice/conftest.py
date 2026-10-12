import pytest


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides NGINX Basic Auth credentials for the ONLYOFFICE browser context.
    Overrides the default (None) from the global conftest.
    """
    return {
        "username": app_credentials["OnlyOffice Username"],
        "password": app_credentials["OnlyOffice Password"],
    }


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote ONLYOFFICE server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the ONLYOFFICE example (test) app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the ONLYOFFICE example app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com/example"
