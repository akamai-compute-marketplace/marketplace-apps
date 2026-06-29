import pytest


@pytest.fixture(scope="session")
def influxdb_admin_credentials(app_credentials) -> dict:
    """
    Returns the InfluxDB admin username and password from the credentials file.
    The key name is dynamic (e.g. 'influxadmin Password') because it is derived
    from the admin_username UDF set at deploy time, so it cannot be hardcoded.

    Returns:
        dict: {'username': str, 'password': str}
    """
    pw_key = next(k for k in app_credentials if k.endswith(" Password") and k != "Sudo Password")
    return {
        "username": pw_key.replace(" Password", ""),
        "password": app_credentials[pw_key],
    }


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote InfluxDB server.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the InfluxDB app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the InfluxDB app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"
