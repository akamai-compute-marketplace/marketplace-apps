import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Grav server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base URL for the Grav site.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Grav site.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def admin_url(base_url) -> str:
    """
    Constructs the admin URL for the Grav site.

    Args:
        base_url: base url

    Returns:
        str: The admin URL of the Grav site.
    """
    return f"{base_url}/admin"
