from playwright.sync_api import expect

from regression_tests.pages.airflow.airflow_login_page import AirflowLoginPage
from regression_tests.pages.airflow.airflow_dashboard_page import AirflowDashboardPage
from regression_tests.pages.airflow.airflow_tech_docs_page import AirflowTechDocsPage


def test_airflow_startup(context, base_url):
    # Verifies that Apache Airflow started and the login page loads successfully.
    login_page = AirflowLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Apache Airflow is not started").to_have_title("Airflow")
    expect(login_page.username_input, "The username input field did not render on the screen.").to_be_visible()


def test_airflow_login(context, base_url, app_credentials):
    # Verifies that user can log in with provided credentials and the DAGs dashboard loads.
    username = app_credentials["Apache Airflow User"]
    password = app_credentials["Apache Airflow Password"]
    login_page = AirflowLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = AirflowDashboardPage(context)
    expect(dashboard_page.dag_runs_header, "DAGs dashboard did not load after login.").to_be_visible(timeout=10000)


def test_airflow_tech_docs(context, techdocs_url):
    """Verify that the Apache Airflow tech docs page is accessible."""
    tech_docs_page = AirflowTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Apache Airflow tech docs page did not load.").to_have_title("Apache Airflow")
    expect(tech_docs_page.airflow_header, "Apache Airflow tech docs header did not render.").to_be_visible()
