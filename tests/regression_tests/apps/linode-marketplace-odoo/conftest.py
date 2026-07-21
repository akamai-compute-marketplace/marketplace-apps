import pytest


@pytest.fixture(scope="session")
def base_url(ssh_credentials) -> str:
    """
    Returns the base URL for the Odoo app.
    Built from the VM host so the suite works against any freshly deployed instance.

    Args:
        ssh_credentials: Tuple of (host, user, password) from env vars.

    Returns:
        str: The base URL of the Odoo app.
    """
    host = ssh_credentials[0]
    linode_host = host.replace(".", "-")
    return f"https://{linode_host}.ip.linodeusercontent.com"


@pytest.fixture(scope="session")
def db_test_data() -> dict:
    """
    Test data used to fill in the one-time Odoo database creation form.

    The database name matches the "Odoo Database name" value from the app's
    credentials file, since that's the name the deploy already expects.

    Returns:
        dict: Field values for OdooDatabaseCreationPage.create_database().
    """
    return {
        "database_name": "odoo",
        "email": "admin@example.com",
        "password": "Str0ng!TestPass_2026",
        "phone": "",
        "language": "English (US)",
        "country": "United States",
        "demo_data": False,
    }
