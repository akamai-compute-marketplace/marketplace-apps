import secrets

import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Plesk server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Plesk admin panel.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Plesk admin panel.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def plesk_initial_login(ssh_credentials) -> dict:
    """
    Returns the one-time, pre-wizard Plesk login: username 'root' with the box's
    system/Linode root password.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        dict: Credentials dict with 'username' and 'password' keys.
    """
    _host, _user, password = ssh_credentials
    return {"username": "root", "password": password}


@pytest.fixture(scope="session")
def plesk_admin_login() -> dict:
    """
    Returns the post-wizard Plesk login: username 'admin' with a freshly generated
    password to be set during the setup wizard.

    Returns:
        dict: Credentials dict with 'username' and 'password' keys.
    """
    return {"username": "admin", "password": secrets.token_urlsafe(16)}
