from playwright.sync_api import expect

from regression_tests.pages.jitsi.jitsi_login_page import JitsiLoginPage
from regression_tests.pages.jitsi.jitsi_prejoin_page import JitsiPrejoinPage
from regression_tests.pages.jitsi.jitsi_meeting_page import JitsiMeetingPage


def test_jitsi_startup(context, base_url):
    # Verifies the app started and the Jitsi Meet landing page loads.
    login_page = JitsiLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Jitsi Meet is not started: page title not found.").to_have_title("Jitsi Meet")
    expect(login_page.heading, "Jitsi Meet heading did not render.").to_be_visible()
    expect(login_page.meeting_name_input, "Meeting name input did not render.").to_be_visible()
    expect(login_page.start_meeting_button, "Start meeting button did not render.").to_be_visible()


def test_jitsi_start_stream(context, base_url):
    # Verifies the user can start a Jitsi meeting and the room stream loads successfully.
    test_room = "test-regression-room"
    login_page = JitsiLoginPage(context)
    login_page.navigate(base_url)
    login_page.start_meeting(test_room)

    prejoin_page = JitsiPrejoinPage(context)
    expect(prejoin_page.heading, "Pre-join screen did not load after starting meeting.").to_be_visible()
    prejoin_page.join("Test User")

    meeting_page = JitsiMeetingPage(context)
    # WebRTC device setup and room connection can take 15–30 s on a fresh instance.
    expect(meeting_page.toolbar_heading, "Meeting room did not load: toolbar not visible.").to_be_visible(timeout=30000)
    expect(meeting_page.leave_meeting_button, "Meeting is not active: leave button not visible.").to_be_visible()
