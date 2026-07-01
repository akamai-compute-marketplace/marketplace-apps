import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote code-server VM.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the code-server app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the code-server app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture
def http_credentials(app_credentials) -> dict:
    """
    Provides HTTP Basic Auth credentials for the code-server browser context.
    Overrides the default (None) from the global conftest.
    code-server is protected by HTTP Basic Auth rather than an in-page login form.
    """
    return {
        "username": app_credentials["Code-Server Login"],
        "password": app_credentials["Code-Server Password"],
    }
