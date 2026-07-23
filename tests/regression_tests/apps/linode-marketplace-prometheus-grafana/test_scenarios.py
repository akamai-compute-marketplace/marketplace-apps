from playwright.sync_api import expect

from regression_tests.pages.prometheus_grafana.prometheus_grafana_login_page import GrafanaLoginPage
from regression_tests.pages.prometheus_grafana.prometheus_grafana_home_page import GrafanaHomePage
from regression_tests.pages.prometheus_grafana.prometheus_grafana_prometheus_page import PrometheusPage
from regression_tests.pages.prometheus_grafana.prometheus_grafana_datasource_page import GrafanaDataSourcePage


def test_prometheus_grafana_grafana_startup(context, base_url):
    # Verifies that Grafana started and the login page loads successfully.
    login_page = GrafanaLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Grafana is not started").to_have_title("Grafana")
    expect(login_page.username_input, "Grafana login form did not render.").to_be_visible()


def test_prometheus_grafana_grafana_login(context, base_url, app_credentials):
    # Verifies that a user can log in to Grafana with the provisioned credentials.
    username = app_credentials["Grafana Username"]
    password = app_credentials["Grafana Password"]
    login_page = GrafanaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = GrafanaHomePage(context)
    expect(home_page.nav_list, "Grafana home page did not load after login.").to_be_visible()


def test_prometheus_grafana_prometheus_startup_and_login(context, base_url):
    # Verifies that Prometheus started and is reachable behind HTTP Basic Auth.
    prometheus_page = PrometheusPage(context)
    prometheus_page.navigate(f"{base_url}/prometheus")
    expect(
        context, "Prometheus is not started"
    ).to_have_title("Prometheus Time Series Collection and Processing Server")
    expect(prometheus_page.execute_button, "Prometheus query page did not render.").to_be_visible()


def test_prometheus_grafana_add_prometheus_data_source(context, base_url, app_credentials):
    # Verifies that Prometheus can be added as a Grafana data source using the
    # in-cluster URL, and that "Save & test" reports success.
    username = app_credentials["Grafana Username"]
    password = app_credentials["Grafana Password"]
    login_page = GrafanaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = GrafanaHomePage(context)
    expect(home_page.nav_list, "Grafana home page did not load after login.").to_be_visible()
    context.wait_for_load_state("networkidle")

    datasource_page = GrafanaDataSourcePage(context)
    datasource_page.navigate(f"{base_url}/connections/datasources/new")
    datasource_page.add_new_prometheus_data_source()
    datasource_page.set_url("http://localhost:9090/prometheus")
    datasource_page.save_and_test()

    expect(
        datasource_page.success_message, "Save & test did not report success."
    ).to_be_visible(timeout=30000)
