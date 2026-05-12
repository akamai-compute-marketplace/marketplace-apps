from playwright.sync_api import expect

from regression_tests.pages.ollama.ollama_chat_page import OllamaChatPage
from regression_tests.pages.ollama.ollama_login_page import OllamaLoginPage


def test_ollama_startup(context, base_url):
    # Verifies that the app started and login page loads successfully.
    login_page = OllamaLoginPage(context)
    login_page.navigate(base_url)
    expect(context, "Ollama is not started").to_have_title("Open WebUI")
    expect(login_page.email_input, "The email input field did not render on the screen.").to_be_visible()


def test_ollama_login(context, base_url, app_credentials):
    # Verifies that user can log in with provided credentials and llama3.2:3b is connected.
    model = "llama3.2:3b"
    username = app_credentials["Open WebUI admin email"]
    password = app_credentials["Open WebUI admin password"]
    login_page = OllamaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    chat_page = OllamaChatPage(context)
    chat_page.hide_release_notes()
    expect(chat_page.chat_input, "Chat is not visible after login.").to_be_visible()
    expect(chat_page.model_selector_input, f"{model} model is not connected").to_contain_text(model)

def test_ollama_chat(context, base_url, app_credentials):
    # Verifies that user can send prompt and get the correct response from model.
    prompt = "What is the capital of France?"
    expected_response = "Paris"
    username = app_credentials["Open WebUI admin email"]
    password = app_credentials["Open WebUI admin password"]
    login_page = OllamaLoginPage(context)
    login_page.navigate(base_url)
    login_page.login(username, password)
    chat_page = OllamaChatPage(context)
    chat_page.hide_release_notes()
    chat_page.send_prompt(prompt)
    expect(chat_page.edit_prompt_button, "Model is not responding after sending a prompt.").to_be_visible(timeout=180000)
    expect(chat_page.prompt_response_field, "Model response is not correct").to_contain_text(expected_response, timeout=180000)
