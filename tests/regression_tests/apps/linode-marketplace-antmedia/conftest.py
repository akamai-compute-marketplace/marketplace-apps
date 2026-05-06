import requests
import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the credentials file on the remote Ant Media Server.

    Returns:
        str: Absolute path to the credentials file.
    """
    print("Using credentials file path...")
    return "../home/admin/.credentials"


@pytest.fixture(scope="session")
def base_url(ssh_credentials):
    """
    Constructs the base HTTPS URL for the Ant Media Server management panel.

    Args:
        ssh_credentials: host

    Returns:
        str: The base URL of the Ant Media Server.
    """
    print("Building base URL for Ant Media Server management panel...")
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com:5443"


@pytest.fixture(scope="session")
def update_codec_settings(base_url, app_credentials):
    """
    Enables VP8 in the LiveApp configuration via the Ant Media Server management REST API.

    Args:
        base_url: The base URL of the Ant Media Server.
        app_credentials: Credentials dict for the Ant Media Server
    """
    print("Enabling VP8 via Ant Media management REST API...")
    email = app_credentials["Ant Media Server Username"]
    password = app_credentials["Ant Media Server Password"]
    settings_url = f"{base_url}/rest/v2/applications/settings/LiveApp"

    session = requests.Session()
    auth_response = session.post(
        f"{base_url}/rest/v2/users/authenticate",
        json={"email": email, "password": password},
        verify=False,
        timeout=30,
    )
    auth_response.raise_for_status()

    response = session.get(settings_url, verify=False, timeout=30)
    response.raise_for_status()
    settings = response.json()

    settings["vp8Enabled"] = True

    response = session.post(settings_url, json=settings, verify=False, timeout=30)
    response.raise_for_status()
