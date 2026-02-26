# Akamai Cloud Compute – Qwen and Open WebUI Deployment One-Click APP

Open WebUI is an open-source, self-hosted web interface for interacting with and managing large language models. It supports multiple AI backends, multi-user access, and extensible integrations, enabling secure and customizable deployment for local or remote model inference.

Our Marketplace application deploys **Qwen instruction-tuned models** as open-weight large language models optimized for reasoning, coding, multilingual understanding, and conversational tasks. Qwen models are designed for efficient inference and integrate seamlessly with self-hosted platforms like Open WebUI, making them well suited for general-purpose assistance, software development workflows, and knowledge-driven use cases.

## Software Included

| Software        | Version      | Description |
| :---            | :----        | :---        |
| Docker    | `29.2.0`    | Container Management Runtime |
| Docker Compose    | `5.0.2`    | Tool for multi-container applications |
| Nginx    | `1.24.0`    | HTTP server used to serve web applications |
| vLLM            | `v0.14.0` tag | Library to run LLM inference models |
| Open WebUI      | `main` tag   | Self-hosted AI interface platform |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name | Description | Actions |
| :--- | :--- | :--- |
| UFW | Add UFW firewalls to the Linode | The UFW module will import a `ufw_rules.yml` provided in `roles/common/tasks` and enables the service. |
| Certbot SSL | Generates and sets auto-renew for Certbot SSL certificates | The Certbot module installs Certbot Python plugin and certificates based on the webserver detected by Ansible. The default renewal cron runs Mondays at 00:00AM and can be manually edited. |
| Fail2Ban | Installs, activates and enables Fail2Ban | The Fail2Ban module installs, activates and enables the Fail2Ban service. |
| Hostname | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Secure SSH | Performs standard SSH hardening | The Secure SSH module writes to `/etc/ssh/sshd_config` to prevent password authentication and enable public key authentication for all users, including root. |
| Sudo User | Creates limited `sudo` user with variable supplied username | Creates limited user from UDF supplied `username`. Note that usernames containing illegal characters will cause the play to fail. |
| SSH Key | Writes SSH pubkey to `sudo` user's `authorized_keys` | Writes UDF supplied `pubkey` to `/home/$username/.ssh/authorized_keys`. To add an SSH key to `root` please use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Update Packages | Performs standard apt updates and upgrades | The Update Packages module performs apt update and upgrade actions as root. |
| GPU Utils | Detects GPU on the instance and installs NVIDIA drivers | Writes `gpu_devices`, `gpu_count`, and `_has_gpu` to `group_vars/linode/vars`. |

# Architecture

## Overview

The Qwen LLM stack consists of two containerized services that work together to provide a complete AI inference platform:

1. **API Service** (`vLLM`) – Model inference and OpenAI-compatible API
2. **UI Service** (`Open WebUI`) – Web-based interface for interacting with the model

Both services are managed via Docker Compose and configured to restart automatically.

## Containerized Services

### API Service (vLLM)

- **Port**: `localhost:8000`
- **Container**: `ghcr.io/vllm-project/vllm-openai:latest`
- **Purpose**: High-performance inference engine for Qwen models
- **Features**:
  - OpenAI-compatible REST API
  - Supports Qwen and other Hugging Face models
  - GPU-accelerated inference
  - Optimized for production workloads

### UI Service (Open WebUI)

- **Port**: `localhost:3000`
- **Container**: `ghcr.io/open-webui/open-webui:main`
- **Purpose**: Browser-based chat and model interaction interface
- **Features**:
  - Browser-based chat UI
  - Persistent chat history and user settings
  - Automatically connects to the API service
  - Multi-user and extensible plugin support

## Web Service

### HTTPS (Nginx)

- **Port**: `443`
- **Features**:
  - HTTPS-secured domain via Let’s Encrypt
  - Reverse proxy for Open WebUI

## Service Communication

The Open WebUI service automatically connects to the vLLM API service running on `localhost:8000`. Both services run on the same instance and communicate over the Docker network.

## Resource Requirements

- **GPU**: Any supported Akamai / Linode GPU instance type
- **Memory**: Varies by Qwen model size (check individual model requirements)
- **Storage**: Sufficient space for model files (Qwen models can be several GB)