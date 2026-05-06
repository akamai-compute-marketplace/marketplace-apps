import pytest

@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Ant Media Server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "../home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials):
    """
    Constructs the base HTTPS URL for the Ant Media Server management panel.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the Ant Media Server (port 5443, HTTPS).
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:5443"
