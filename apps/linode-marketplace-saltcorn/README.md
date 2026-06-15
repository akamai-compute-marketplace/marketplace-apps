# Akamai Cloud Compute – Saltcorn Quick Deploy App

Saltcorn is an open-source, self-hosted no-code database application builder that allows users to create web applications without writing code. It features a completely flexible database schema, a rich ecosystem of pluggable extensions, a drag-and-drop view builder, and a granular access control system, making it ideal for building custom CRMs, project management tools, tracking systems, and operational dashboards.

## Software Included

| Software | Version | Description |
| :--- | :---- | :--- |
| Saltcorn | `latest stable` | No-code database application builder |
| Node.js | `24` | Tool for multi-container applications |
| Nginx | `1.24.0` | HTTP server used to serve web applications |


**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name | Description | Actions |
| :--- | :--- | :--- |
| UFW | Firewall Management | Configures `ufw_rules.yml` to allow ports **80**, **443**, and **22**. |
| Fail2Ban | Security Hardening | Installs and enables Fail2Ban to monitor logs and block malicious IP addresses. |
| Hostname | FQDN Assignment | Assigns a hostname to the Linode based on UDF domains or default rDNS for SSL validity. |
| Secure SSH | SSH Hardening | Disables password authentication and enforces public key authentication. |
| Sudo User | User Creation | Creates a limited `sudo` user with a custom username for administrative tasks. |
| Update Packages | System Updates | Performs `apt update` and `apt upgrade` to ensure the OS is patched. |

# Architecture

## Overview

The Saltcorn deployment pulls in the @saltcorn/cli package (equivalent to npm install -g @saltcorn/cli), which itself is the entry point for the whole platform. Saltcorn is a monorepo, and the CLI brings along these core packages:

- **@saltcorn/data** — the core of the project, handling the definition of entities (tables, fields, pages, etc.) and their persistence to a database. Saltcorn
- **@saltcorn/markup** — utilities to help create HTML markup from JavaScript, built around a tags module that exports functions generating HTML. Saltcorn
- **@saltcorn/server** — defines the routes and the core HTTP server process, handling both administration and serving data to users; based on the Express framework. Saltcorn
- **@saltcorn/cli** — code for the saltcorn command-line interface executable, based on the oclif framework. Saltcorn
- **saltcorn-builder** — the drag-and-drop builder used to build pages and views; it's a React component compiled separately, with its build artifact (dist/builder_bundle.js) included in the npm package.

## Resource Requirements

- **Recommended**: 4GB Dedicated CPU or Shared Compute instance.
- **Storage**: At least 30GB to accommodate MongoDB journals, file uploads, and Docker image layers.
- **Network**: A valid domain name (FQDN) is required for Nginx to successfully provision SSL certificates (This deployment can use the default RDNS address as a valid domain if no domain is specified).