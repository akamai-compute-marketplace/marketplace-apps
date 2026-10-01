import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the OpenLiteSpeed credentials file.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the sample Node.js application.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The HTTPS application URL.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def admin_url(ssh_credentials) -> str:
    """
    Returns the URL for the OpenLiteSpeed WebAdmin console.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The HTTPS WebAdmin URL.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:7080"
