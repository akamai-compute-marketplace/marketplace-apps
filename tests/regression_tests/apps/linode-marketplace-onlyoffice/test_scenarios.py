from playwright.sync_api import expect

from regression_tests.pages.onlyoffice.onlyoffice_editor_page import OnlyofficeEditorPage
from regression_tests.pages.onlyoffice.onlyoffice_example_page import OnlyofficeExamplePage
from regression_tests.pages.onlyoffice.onlyoffice_tech_docs_page import OnlyofficeTechDocsPage


def test_onlyoffice_startup(context, base_url):
    # Verifies that the app started: there is no login page, so startup is confirmed by passing HTTP Basic Auth.
    example_page = OnlyofficeExamplePage(context)
    example_page.navigate(base_url)
    expect(context, "ONLYOFFICE example app title did not match.").to_have_title("ONLYOFFICE Document Editors")
    expect(example_page.create_document_link, "'Create new Document' link did not render.").to_be_visible()


def test_onlyoffice_open_sample_document(context, base_url):
    # Verifies that a document with sample content opens in the editor.
    example_page = OnlyofficeExamplePage(context)
    example_page.navigate(base_url)
    editor_page = OnlyofficeEditorPage(example_page.create_document(with_sample_content=True))
    expect(editor_page.page, "Sample document editor title did not match.").to_have_title(
        "sample.docx - ONLYOFFICE", timeout=60000
    )
    expect(editor_page.document_name_input, "Editor did not show the sample document name.").to_have_value(
        "sample.docx", timeout=60000
    )
    expect(editor_page.document_area, "Document editing area did not render.").to_be_visible()
    expect(editor_page.page_counter, "Sample document pages were not loaded.").to_contain_text("Page 1 of")


def test_onlyoffice_create_new_document(context, base_url):
    # Verifies that creating a new document adds it to the stored documents list.
    example_page = OnlyofficeExamplePage(context)
    example_page.navigate(base_url)
    example_page.create_document(with_sample_content=False)
    context.bring_to_front()
    expect(example_page.stored_file("new.docx"), "New document is not shown in 'Your documents'.").to_be_visible(
        timeout=30000
    )


def test_onlyoffice_tech_docs(context, techdocs_url):
    """Verify that the ONLYOFFICE tech docs page is accessible."""
    tech_docs_page = OnlyofficeTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "ONLYOFFICE tech docs title did not match.").to_have_title("ONLYOFFICE Docs")
    expect(tech_docs_page.onlyoffice_header, "ONLYOFFICE tech docs header did not render.").to_be_visible()
