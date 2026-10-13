from playwright.sync_api import expect

from regression_tests.pages.ruby_rails.ruby_rails_home_page import RubyRailsHomePage
from regression_tests.pages.ruby_rails.ruby_rails_tech_docs_page import RubyRailsTechDocsPage


def test_ruby_rails_startup(context, base_url):
    """Verifies that the Ruby on Rails app started and the landing page loads successfully."""
    home_page = RubyRailsHomePage(context)
    home_page.navigate(base_url)
    expect(context, "Ruby on Rails app is not started").to_have_title("Linode Marketplace Ruby Rails")
    expect(home_page.heading, "Landing page heading did not render.").to_be_visible()


def test_ruby_rails_tech_docs(context, techdocs_url):
    """Verify that the Ruby on Rails tech docs page is accessible."""
    tech_docs_page = RubyRailsTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Ruby on Rails tech docs page title is incorrect.").to_have_title("Ruby on Rails")
    expect(tech_docs_page.ruby_rails_header, "Ruby on Rails tech docs header did not render.").to_be_visible()
