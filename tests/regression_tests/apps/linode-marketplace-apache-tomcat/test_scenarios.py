import uuid

import pytest
from playwright.sync_api import expect

from regression_tests.pages.apache_tomcat.apache_tomcat_tech_docs_page import ApacheTomcatTechDocsPage
from regression_tests.services.apache_tomcat.apache_tomcat_service import ApacheTomcatService


def test_apache_tomcat_up(remote_exec):
    # Verifies that the Tomcat service is active and runs as the unprivileged tomcat user.
    service = ApacheTomcatService(remote_exec)
    assert service.unit_active() == "active", "tomcat unit is not active"
    assert service.process_user() == "tomcat", "Tomcat JVM is not running as the tomcat user"


def test_apache_tomcat_serves_default_page(remote_exec, http_session, base_url):
    # Verifies that Tomcat serves the bundled sample application at the root over HTTPS.
    service = ApacheTomcatService(remote_exec, http_session, base_url)
    response = service.get("/")
    assert response.status_code == 200, f"root page returned {response.status_code}"
    assert 'Sample "Hello, World" Application' in response.text, "root page did not render the sample application"


def test_apache_tomcat_deploys_war(remote_exec, http_session, base_url):
    # Verifies that a WAR dropped into webapps is hot-deployed and its servlet and JSP respond.
    service = ApacheTomcatService(remote_exec, http_session, base_url)
    app_name = f"sample-{uuid.uuid4().hex[:8]}"
    _, err, code = service.deploy_war("ROOT.war", app_name)
    assert code == 0, f"copying the WAR failed: {err}"
    assert service.wait_until_served(f"/{app_name}/hello"), f"/{app_name} was not deployed within 60s"
    servlet = service.get(f"/{app_name}/hello")
    assert "<h1>Sample Application Servlet</h1>" in servlet.text, "sample servlet did not render"
    jsp = service.get(f"/{app_name}/hello.jsp")
    assert "<h1>Sample Application JSP Page</h1>" in jsp.text, "sample JSP did not render"


@pytest.mark.xfail(reason="Tech docs page is not ready yet")
def test_apache_tomcat_tech_docs(context, techdocs_url):
    """Verify that the Apache Tomcat tech docs page is accessible."""
    tech_docs_page = ApacheTomcatTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "Apache Tomcat tech docs page did not load.").to_have_title("Apache Tomcat")
    expect(tech_docs_page.apache_tomcat_header, "Apache Tomcat tech docs header did not render.").to_be_visible()
