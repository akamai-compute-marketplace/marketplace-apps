from playwright.sync_api import expect

from regression_tests.pages.jupyterlab.jupyterlab_login_page import JupyterlabLoginPage
from regression_tests.pages.jupyterlab.jupyterlab_lab_page import JupyterlabLabPage
from regression_tests.pages.jupyterlab.jupyterlab_notebook_page import JupyterlabNotebookPage


def test_jupyterlab_startup(context, base_url):
    # Verifies the app started and the JupyterLab login page loads successfully.
    login_page = JupyterlabLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "JupyterLab is not started: page title not found.").to_have_title("Jupyter Server")
    expect(login_page.token_input, "Token input did not render.").to_be_visible()
    expect(login_page.login_button, "Log in button did not render.").to_be_visible()


def test_jupyterlab_login(context, base_url, app_credentials):
    # Verifies that the user can log in with the Jupyter token and the lab workspace loads.
    token = app_credentials["Jupyter Token"]
    login_page = JupyterlabLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(token)
    lab_page = JupyterlabLabPage(context)
    expect(context, "JupyterLab workspace did not load after login.").to_have_title("JupyterLab")
    expect(lab_page.file_menu, "File menu not visible — workspace may not have loaded.").to_be_visible()


def test_jupyterlab_run_notebook(context, base_url, app_credentials):
    # Logs in, creates a new Python 3 notebook, runs print("hello"), and verifies the output.
    token = app_credentials["Jupyter Token"]
    login_page = JupyterlabLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(token)
    lab_page = JupyterlabLabPage(context)
    expect(context, "JupyterLab workspace did not load.").to_have_title("JupyterLab")
    lab_page.new_launcher_button.click()
    lab_page.notebook_python3_button.click()
    notebook_page = JupyterlabNotebookPage(context)
    expect(notebook_page.run_cell_button, "Notebook toolbar not visible: notebook may not have opened.").to_be_visible()
    notebook_page.active_cell_input.fill('print("hello")')
    notebook_page.run_cell_button.click()
    expect(notebook_page.notebook_content, "Cell output did not appear after running print('hello').").to_contain_text("hello")
