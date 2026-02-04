# Akamai Cloud Compute - PostgreSQL with PGVector Deployment One-Click APP

PostgreSQL is a powerful, open-source relational database system known for its reliability, extensibility, and performance. PGVector is a PostgreSQL extension that enables efficient storage and similarity search over vector embeddings, making it ideal for AI, machine learning, and retrieval-augmented generation (RAG) workloads.

Our Marketplace application deploys a **production-ready, PostgreSQL installation** with the PGVector extension installed and enabled directly on the host. This solution follows industry best practices for security, performance tuning, and persistence, and is suitable for use as a primary database backend for AI-driven applications.

## Software Included

| Software   | Version | Description |
| :---       | :----   | :---        |
| PostgreSQL | `16`    | Open-source relational database |
| PGVector   | `0.8.x` | PostgreSQL extension for vector similarity search |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name | Description | Actions
| :--- | :---        | :---
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/common/tasks` and enables the service.  |
| Certbot SSL   | Generates and sets auto-renew for Certbot SSL certificates  | The Certbot module installs Certbot Python plugin and certificates based on the detected services. |
| Fail2Ban   | Installs, activates and enables Fail2Ban  | The Fail2Ban module installs, activates and enables the Fail2Ban service.   |
| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Secure SSH   | Performs standard SSH hardening.  | The Secure SSH module writes to `/etc/ssh/sshd_config` to prevent password authentication and enable public key authentication for all users, including root.  |  
| Sudo User  | Creates limited `sudo` user with variable supplied username.  | Creates limited user from UDF supplied `username.` Note that usernames containing illegal characters will cause the play to fail. |
| SSH Key   | Writes SSH pubkey to `sudo` user's `authorized_keys`.  | Writes UDF supplied `pubkey` to `/home/$username/.ssh/authorized_keys`. To add a SSH key to `root` please use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/).   |
| Update Packages   | Performs standard apt updates and upgrades. | The Update Packages module performs apt update and upgrade actions as root.  |

# Architecture

## Overview

The PostgreSQL with PGVector deployment consists of a **single, host-installed database service** optimized for transactional and vector-based workloads:

1. **Database Service** (`PostgreSQL + PGVector`): Relational and vector database engine

The service is installed directly on the system, managed by `systemd`, and configured to start automatically on boot.

## Services

### Database Service (PostgreSQL + PGVector)

- **Port**: `5432`
- **Service Name**: `postgresql`
- **Purpose**: Relational database with native vector similarity search
- **Features**:
  - PostgreSQL 16 installed from official repositories
  - PGVector extension enabled by default
  - Support for `vector` data types and similarity indexes (IVFFlat, HNSW)
  - ACID-compliant transactional storage
  - Optimized configuration for production workloads

## Service Communication

Client applications connect directly to PostgreSQL over TCP on port `5432`. Network access is restricted by UFW firewall rules, and secure authentication is enforced using PostgreSQL role-based access control. TLS can be enabled for encrypted client connections when required.

## Resource Requirements

- **CPU**: Scales with query complexity and indexing workload
- **Memory**: Recommended 8GB+ for vector-heavy workloads
- **Storage**: Depends on dataset size, vector dimensionality, and index type

## Vector Search and AI Workloads

PGVector enables efficient similarity search over embedding vectors stored directly within PostgreSQL tables. This allows applications to combine traditional relational queries with vector-based semantic search in a single database, making it ideal for RAG pipelines, recommendation systems, and AI-powered search workloads.
