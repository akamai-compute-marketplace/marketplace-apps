from playwright.sync_api import expect

from regression_tests.pages.mistral.mistral_chat_page import MistralChatPage
from regression_tests.pages.mistral.mistral_login_page import MistralLoginPage


def test_mistral_startup(context, base_url):
    # Verifies that the app started and login page loads successfully.
    login_page = MistralLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Mistral is not started").to_have_title("Open WebUI")
    expect(login_page.email_input, "The email input field did not render on the screen.").to_be_visible()


def test_mistral_login(context, base_url, app_credentials):
    # Verifies that user can log in with provided credentials and mistralai/Mistral-7B-Instruct-v0.3 is connected.
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    username = app_credentials["Open WebUI admin email"]
    password = app_credentials["Open WebUI admin password"]
    login_page = MistralLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    chat_page = MistralChatPage(context)
    chat_page.hide_release_notes()
    chat_page.select_model(model)
    expect(chat_page.chat_input, "Chat is not visible after login.").to_be_visible()
    expect(chat_page.model_selector_input, f"{model} model is not connected").to_contain_text(model)

def test_mistral_chat(context, base_url, app_credentials):
    # Verifies that user can send prompt and get the correct response from model.
    model = "mistralai/Mistral-7B-Instruct-v0.3"
    prompt = "What is the capital of France?"
    expected_response = "Paris"
    username = app_credentials["Open WebUI admin email"]
    password = app_credentials["Open WebUI admin password"]
    login_page = MistralLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    chat_page = MistralChatPage(context)
    chat_page.hide_release_notes()
    chat_page.select_model(model)
    chat_page.send_prompt(prompt)
    expect(chat_page.edit_prompt_button, "Model is not responding after sending a prompt.").to_be_visible(timeout=180000)
    expect(chat_page.prompt_response_field, "Model response is not correct").to_contain_text(expected_response, timeout=180000)
