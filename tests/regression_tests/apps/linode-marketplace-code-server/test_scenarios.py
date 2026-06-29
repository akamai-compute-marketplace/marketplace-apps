from playwright.sync_api import expect

from regression_tests.pages.code_server.code_server_main_page import CodeServerMainPage
from regression_tests.pages.code_server.code_server_explorer_page import CodeServerExplorerPage


def test_code_server_login(context, base_url):
    """Verifies that HTTP Basic Auth credentials are accepted and the full editor UI is accessible."""
    login_page = CodeServerMainPage(context)
    login_page.navigate(base_url)
    expect(login_page.status_bar, "Status bar is not visible — HTTP Basic Auth may have failed.").to_be_visible()
    expect(login_page.view_switcher, "View switcher is not visible after authenticated access.").to_be_visible()


def test_code_server_create_file(context, base_url):
    """
    Verifies that a new file can be created via the Explorer panel and
    immediately appears in the folder tree.
    """
    filename = "test_regression.txt"
    explorer_page = CodeServerExplorerPage(context)

    # Open the /home/admin folder
    explorer_page.open_folder(base_url)

    # Accept the workspace trust dialog (shown on first open of the folder)
    explorer_page.handle_trust_dialog()

    # Wait for the Explorer section to be ready, then create the file
    explorer_page.wait_for_explorer()
    explorer_page.create_new_file(filename)

    # Verify the new file is visible in the Explorer tree
    file_item = explorer_page.get_file_item(filename)
    expect(file_item, f"File '{filename}' was not found in the Explorer after creation.").to_be_visible()
