import pytest


@pytest.fixture(scope="session")
def credentials_file_path():
    """
    Returns the path to the NemoClaw deployment credentials.

    Returns:
        str: Absolute path to the credentials file.
    """
    return "/home/admin/.credentials"
