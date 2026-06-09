import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Joomla.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "../home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Constructs the base URL for the Joomla.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the Joomla.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def admin_url(base_url) -> str:
    """
    Constructs the administrator URL for the Joomla.

    Args:
        base_url: base url

    Returns:
        str: The administrator URL of the Joomla.
    """
    return f"{base_url}/administrator"
