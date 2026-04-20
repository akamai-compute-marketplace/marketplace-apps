# GitHub Actions CI/CD Workflows

This directory contains the GitHub Actions workflows and supporting scripts that power the CI/CD pipeline for Marketplace Apps.

---

## Workflows

### 1. Development Workflow (`development.yml`)

**Trigger:** 
- Pull request creation or update against `target` branch (e.g. `main` or `develop`)
- Manual run for branch against `main` branch

**Scope:** Compares changed files in `apps/` and `deployment_scripts/` against `target` branch. Only apps with a `deployment_scripts/<app>/linode-config.sh` are deployed.

**Purpose:** Validates and deploys any new or updated apps.


---

### 2. Scheduled Workflow (`scheduled.yml`)

**Trigger:**
- Weekly cron schedule — every **Sunday at 18:00 UTC**
- Manual run

**Scope:** Deploys and runs **all apps** on the `main` branch.

**Purpose:** Regression testing and ensuring all apps remain functional over time.

---

### 3. Dependency Updates (`dependency-updates.yml`)

**Trigger:**
- Scheduled cron — e.g., 15th of every month at 09:00 UTC
- Manual run

**Scope:** Scans `requirements.txt` and `collections.yml` files across all apps in the repository.

**Purpose:** Automates dependency lifecycle management. It queries PyPI and Ansible Galaxy for the latest stable versions, safely bumps pinned versions, and opens a consolidated Pull Request containing detailed Markdown tables of all updates.

---

## Deployment Job Flow

Each app in the matrix goes through the following steps:

```
linode-config.sh                   → Load app-specific Linode configuration (region, type, image, etc.)
linode-provisioning.sh             → Create a Linode instance and wait for it to be ready
app-installation.sh                → SSH into the Linode, clone the repo, and run the deployment script
linode-deletion.sh                 → Delete the Linode instance (always runs, even on failure)
teardown-domain-records-cleanup.sh → Remove DNS records created during deployment (always runs)
```

---

## Required Secrets & Variables

| Name | Type | Description |
|------|------|-------------|
| `LINODE_API_SECRET` | Secret | Linode API token used for provisioning and DNS management |
| `LINODE_ROOT_PASS` | Secret | Root password set on provisioned Linode instances |
| `HF_TOKEN` | Secret | Hugging Face API token (used by AI/ML apps) |
| `LINODE_DOMAIN` | Variable | Base domain used for app DNS records |
| `LINODE_SUBDOMAIN` | Variable | Subdomain prefix used for app DNS records |
| `DEPS_APP_ID` | Secret | GitHub App ID used for authenticating dependency updates |
| `DEPS_APP_SECRET` | Secret | GitHub App private key used for authenticating dependency updates |

---

## Scripts

All supporting scripts live in `.github/scripts/`:

| Script | Description |
|--------|-------------|
| `get-all-apps.sh` | Lists all apps under `deployment_scripts/` that have a `linode-config.sh` |
| `get-updated-apps.sh` | Lists apps with changes vs `main` that have a `linode-config.sh` |
| `setup-domain-records-cleanup.sh` | Pre-deployment DNS cleanup |
| `teardown-domain-records-cleanup.sh` | Post-deployment DNS cleanup |
| `linode-provisioning.sh` | Creates a Linode instance and outputs `LINODE_IPV4` and `LINODE_ID` |
| `app-installation.sh` | Connects via SSH and runs the app deployment |
| `linode-deletion.sh` | Deletes a Linode instance by ID |
| `static-code-shellcheck.sh` | Runs ShellCheck across the repository |
| `static-code-yamllint.sh` | Runs yamllint across the repository |
| `static-code-ansible-lint.sh` | Runs ansible-lint across the repository |
| `python-deps-check.py` | Queries PyPI and records available Python package updates |
| `ansible-deps-check.py` | Queries Ansible Galaxy v3 API and records Ansible collection updates |
| `generate-pr-body.py` | Parses dependency update reports to generate a unified Markdown PR body |

---

## App Structure

Each app must follow this structure to be picked up by the pipeline:

```
deployment_scripts/
  <app-name>/
    linode-config.sh     ← required: defines REGION, LINODE_TYPE, IMAGE, etc.
    <deploy-script>.sh   ← deployment entry point

apps/
  <app-name>/            ← Ansible roles and playbooks
```

