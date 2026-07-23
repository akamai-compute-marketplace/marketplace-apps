import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote MERN server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the MERN Express API (nginx + TLS on 443, self-signed).
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the MERN app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"
