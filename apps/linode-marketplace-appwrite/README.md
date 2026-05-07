# Akamai Cloud Compute – Appwrite Deployment One-Click APP (MongoDB & Traefik Edition)

Appwrite is an open-source, self-hosted Backend-as-a-Service (BaaS) platform that provides developers with a set of tools and APIs to build web and mobile applications faster. It handles common backend tasks including user authentication, database management, file storage, serverless functions, and real-time event subscriptions.

This Marketplace application deploys **Appwrite** as a fully containerized stack using Docker Compose, fronted by **Traefik** for modern edge routing, automatic SSL orchestration via Let's Encrypt, and high-performance load balancing. This configuration replaces the traditional Nginx/MariaDB setup with a **MongoDB** backend for flexible, document-oriented data storage.

## Software Included

| Software | Version | Description |
| :--- | :---- | :--- |
| Docker | `29.4.2` | Container Management Runtime |
| Docker Compose | `5.1.3` | Tool for multi-container applications |
| Traefik | `3.6` | Edge router, reverse proxy, and SSL orchestrator |
| Appwrite | `1.9.0` tag | Open-source Backend-as-a-Service platform |
| MongoDB | `8.2.5` | NoSQL document database used by Appwrite |
| Redis | `7.4.7` | In-memory cache and queue for Appwrite |
| OpenRuntimes Executor | `0.7.22` | Serverless function execution runtime |

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

The Appwrite stack consists of multiple containerized services optimized for performance and scalability:

1.  **Core Service** (`appwrite`) – REST API, authentication, and core logic.
2.  **Realtime Service** (`appwrite-realtime`) – WebSocket-based event subscriptions.
3.  **Worker Services** – Background job processing for audits, webhooks, builds, and messaging.
4.  **Executor** (`openruntimes-executor`) – Serverless function runtime.
5.  **MongoDB** – Primary persistent NoSQL database for flexible data modeling.
6.  **Redis** – High-speed cache and message broker for the internal queue.
7.  **Traefik** – The entry point for all traffic, managing SSL termination and routing.

## Containerized Services

### Core Service (Appwrite)
- **Image**: `appwrite/appwrite:1.9.0`
- **Internal Routing**: Traefik handles routing via Docker labels.
- **Features**: REST/GraphQL APIs, Auth, Storage, and Functions.

### Database (MongoDB)
- **Container**: `mongo:8.2.5`
- **Purpose**: Persistent storage. MongoDB provides a flexible schema ideal for rapidly evolving application data.

### Edge Router (Traefik)
- **Container**: `traefik:3.6`
- **Ports**: `80`, `443`, and `8080` (optional dashboard).
- **Purpose**: Dynamically discovers containers and secures them with Let's Encrypt certificates automatically.

### Cache / Queue (Redis)
- **Container**: `redis:7.4.7-alpine`
- **Purpose**: Session management, task queuing, and real-time Pub/Sub.

## Traffic Management

### HTTPS (Traefik)
- **Entry Points**: Port 80 (redirects to 443) and Port 443.
- **SSL**: Automated via Let's Encrypt using the HTTP-01 challenge.
- **Routing**: Uses container labels to define middleware (compression, headers) and service routing.

## Resource Requirements

- **Recommended**: 8GB Dedicated CPU or Shared Compute instance.
- **Storage**: At least 30GB to accommodate MongoDB journals, file uploads, and Docker image layers.
- **Network**: A valid domain name (FQDN) is required for Traefik to successfully provision SSL certificates (This deployment can use the default RDNS address as a valid domain if no domain is specified).