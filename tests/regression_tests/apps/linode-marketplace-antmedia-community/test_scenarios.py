from playwright.sync_api import expect
from regression_tests.pages.antmedia_community.dashboard_page import DashboardPage
from regression_tests.pages.antmedia_community.login_page import LoginPage
from regression_tests.pages.antmedia_community.stream_page import StreamPage


def test_antmedia_startup(context, base_url):
    # Verifies that the Ant Media Server started and login page loads successfully.
    login_page = LoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Ant Media Server is not started").to_have_title("Management of Ant Media Server")
    expect(login_page.username_input, "The username input field did not render on the screen.").to_be_visible()


def test_antmedia_login(context, base_url, app_credentials):
    # Verifies that user can loging to And Media Server with provided credentials.
    username = app_credentials["Ant Media Server Username"]
    password = app_credentials["Ant Media Server Password"]
    login_page = LoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = DashboardPage(context)
    expect(dashboard_page.active_live_streams_label, "Credentials are invalid or something went wrong").to_be_visible()


def test_antmedia_start_stream(context, base_url, app_credentials):
    # Verifies that user can start a WebRTC stream.
    username = app_credentials["Ant Media Server Username"]
    password = app_credentials["Ant Media Server Password"]
    login_page = LoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    dashboard_page = DashboardPage(context)
    web_rtc_stream_url = f"{base_url}/WebRTCApp/index.html"
    new_page = dashboard_page.open_new_tab()
    stream_page = StreamPage(new_page)
    stream_page.navigate(web_rtc_stream_url)
    expect(stream_page.stream_frame.status_offline_label, "WebRTCApp is not available").to_be_visible()
    stream_page.stream_frame.start_publishing()
    expect(stream_page.stream_frame.status_online_label, "Stream is not started").to_be_visible()
    expect(dashboard_page.active_live_streams_label, "Stream info is not displayed on the dashboard").to_contain_text(
        "Active Live Streams 1")
