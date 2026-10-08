from playwright.sync_api import expect
from regression_tests.pages.hashicorp_nomad.nomad_jobs_page import NomadJobsPage
from regression_tests.pages.hashicorp_nomad.nomad_profile_page import NomadProfilePage
from regression_tests.pages.hashicorp_nomad.nomad_tech_docs_page import NomadTechDocsPage


def test_nomad_anonymous_token(context, base_url):
    # Verifies that the HashiCorp Nomad is started and user can log in with basic auth credentials
    jobs_page = NomadJobsPage(context)
    jobs_page.navigate(base_url)
    expect(context, "Nomad is not started").to_have_title("Nomad")
    expect(jobs_page.message_label, "Can not log in with basic auth credentials").to_contain_text("Not Authorized")


def test_nomad_management_token(context, base_url, app_credentials):
    # Verifies that user can log in with Nomad Management Token
    secret = app_credentials["Nomad Management Token (Secret ID)"]
    jobs_page = NomadJobsPage(context)
    jobs_page.navigate(base_url)
    expect(jobs_page.message_label, "Can not log in with basic auth credentials").to_contain_text("Not Authorized")
    jobs_page.sign_out()
    jobs_page.go_to_profile_page()
    profile_page = NomadProfilePage(context)
    profile_page.sign_in_with_secret(secret)
    expect(profile_page.auth_success_message, "Can not log in with Nomad Management Token").to_be_visible()


def test_nomad_job_deployment(context, base_url, app_credentials, job_definition):
    # Verifies that job is deployed and running
    secret = app_credentials["Nomad Management Token (Secret ID)"]
    jobs_page = NomadJobsPage(context)
    jobs_page.navigate(base_url)
    expect(jobs_page.message_label, "Can not log in with basic auth credentials").to_contain_text("Not Authorized")
    jobs_page.sign_out()
    jobs_page.go_to_profile_page()
    profile_page = NomadProfilePage(context)
    profile_page.sign_in_with_secret(secret)
    expect(profile_page.auth_success_message, "Can not log in with Nomad Management Token").to_be_visible()
    profile_page.go_to_jobs_page()
    jobs_page.setup_and_run_job(job_definition)
    expect(jobs_page.job_status_badge, "Job did not become healthy").to_have_text("Healthy", timeout=120000)


def test_hashicorp_nomad_tech_docs(context, techdocs_url):
    """Verify that the HashiCorp Nomad tech docs page is accessible."""
    tech_docs_page = NomadTechDocsPage(context)
    tech_docs_page.navigate(techdocs_url)
    expect(context, "HashiCorp Nomad tech docs page did not load.").to_have_title("HashiCorp Nomad")
    expect(tech_docs_page.hashicorp_nomad_header, "HashiCorp Nomad tech docs header did not render.").to_be_visible()
