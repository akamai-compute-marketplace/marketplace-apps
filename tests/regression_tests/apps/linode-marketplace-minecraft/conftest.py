import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """Return the Minecraft credentials file path on the remote server."""
    return "/home/admin/.credentials"
