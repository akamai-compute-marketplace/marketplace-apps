import re

from playwright.sync_api import expect

from regression_tests.pages.influxdb.influxdb_login_page import InfluxDBLoginPage
from regression_tests.pages.influxdb.influxdb_home_page import InfluxDBHomePage
from regression_tests.pages.influxdb.influxdb_buckets_page import InfluxDBBucketsPage


def test_influxdb_startup(context, base_url):
    # Verifies that the app started and the login page loads successfully.
    login_page = InfluxDBLoginPage(context)
    login_page.navigate(f"{base_url}/signin")
    expect(context, "InfluxDB is not started").to_have_title("InfluxDB")
    expect(login_page.username_input, "Login form did not render.").to_be_visible(timeout=30000)


def test_influxdb_login(context, base_url, influxdb_admin_credentials):
    # Verifies that the admin user can log in with the provided credentials.
    username = influxdb_admin_credentials["username"]
    password = influxdb_admin_credentials["password"]
    login_page = InfluxDBLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = InfluxDBHomePage(context)
    expect(home_page.get_started_heading, "Dashboard did not load after login.").to_be_visible()


def test_influxdb_create_bucket(context, base_url, influxdb_admin_credentials):
    # Verifies that the admin can create a bucket and it appears in the bucket list.
    username = influxdb_admin_credentials["username"]
    password = influxdb_admin_credentials["password"]
    bucket_name = "test-automation-bucket"
    login_page = InfluxDBLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    home_page = InfluxDBHomePage(context)
    home_page.get_started_heading.wait_for()
    org_id = re.search(r"/orgs/([^/]+)", context.url).group(1)

    buckets_page = InfluxDBBucketsPage(context)
    buckets_page.navigate(f"{base_url}/orgs/{org_id}/load-data/buckets")
    buckets_page.create_bucket(bucket_name)
    expect(buckets_page.get_bucket_item(bucket_name), "Created bucket did not appear in the list.").to_be_visible()
