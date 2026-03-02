# Akamai Cloud Compute - Gemma 3 and Open WebUI Deployment One-Click App

Open WebUI is an open-source, self-hosted web interface for interacting with and managing large language models. It supports multiple AI backends, multi-user access, and extensible integrations, enabling secure and customizable deployment for local or remote model inference.

Our Marketplace application deploys Google Gemma 3, a state-of-the-art open-source large language model with multimodal understanding and multilingual capabilities. Built from the same technology that powers Google's Gemini models, Gemma 3 is optimized for instruction following, reasoning, and conversational tasks while maintaining efficient inference performance.

During deployment, you can choose between two model sizes to match your GPU capabilities and performance requirements. See **Resource Requirements** below.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Docker    | `29.1.3`    | Container Management Runtime |
| Docker Compose    | `1.29.2`    | Tool for multi-container applications |
| Nginx    | `1.24.0`    | HTTP server used to serve web applications |
| vLLM | `latest` tag | Library to run LLM inference models  |
| Open WebUI | `main` tag | Self-hosted AI interface platform |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name | Description | Actions
| :--- | :---        | :---
| UFW   | Add UFW firewalls to the Linode  | The UFW module will import a `ufw_rules.yml` provided in `roles/common/tasks` and enables the service.  |
| Certbot SSL   | Generates and sets auto-renew for Certbot SSL certificates  | The Certbot module installs Certbot Python plugin and certificates based on the webserver detected by Ansible. The default renewal cron runs Mondays at 00:00AM and can be manually edited. |
| Fail2Ban   | Installs, activates and enables Fail2Ban  | The Fail2Ban module installs, activates and enables the Fail2Ban service.   |
| Hostname   | Assigns a hostname to the Linode based on domains provided via UDF or uses default rDNS. | The Hostname module accepts a UDF to assign a FQDN and write to the `/etc/hosts` file. If no domain is provided the default `ip.linodeusercontent.com` rDNS will be used. For consistency, DNS and SSL configurations should use the Hostname generated `_domain` var when possible. |
| Secure SSH   | Performs standard SSH hardening.  | The Secure SSH module writes to `/etc/ssh/sshd_config` to prevent password authentication and enable public key authentication for all users, including root.  |
| Sudo User  | Creates limited `sudo` user with variable supplied username.  | Creates limited user from UDF supplied `username.` Note that usernames containing illegal characters will cause the play to fail. |
| SSH Key   | Writes SSH pubkey to `sudo` user's `authorized_keys`.  | Writes UDF supplied `pubkey` to `/home/$username/.ssh/authorized_keys`. To add a SSH key to `root` please use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/).   |
| Update Packages   | Performs standard apt updates and upgrades. | The Update Packages module performs apt update and upgrade actions as root.  |
| GPU Utils| Detects GPU on the instance and install NVIDIA drivers | Writes `gpu_devices`, `gpu_count`, and `_has_gpu` to `group_vars/linode/vars` |

# Architecture

## Overview

The Gemma 3 LLM consists of two containerized services that work together to provide a complete AI inference stack:

1. **API Service** (`vLLM`): High-performance inference engine
2. **UI Service** (`Open WebUI`): Feature-rich chat interface

Both services are managed via Docker Compose and configured to restart automatically.

## Containered Services

### API Service (vLLM)

- **Port**: `localhost:8000`
- **Container**: `vllm/vllm-openai:latest`
- **Model**: `google/gemma-3-4b-it` or `google/gemma-3-12b-it` (user selectable)
- **Purpose**: High-performance inference engine with OpenAI-compatible REST API
- **Features**:
  - OpenAI-compatible REST API
  - GPU-accelerated inference
  - Supports Hugging Face gated models
  - Optimized for production workloads
  - 16,384 token context length

### UI Service (Open WebUI)

- **Port**: `localhost:3000`
- **Container**: `ghcr.io/open-webui/open-webui:main`
- **Purpose**: Browser-based chat interface
- **Features**:
  - Browser-based chat UI
  - Persistent chat history
  - Connected to the API service automatically
  - User-friendly interface for interacting with models

## Web Service

### HTTPS (Nginx)

- **port**: 443
- **Features**:
  - HTTPS Secured domain via Let's Encrypt

## Directory Structure

The following directories are used on the deployed instance:

- `/opt/gemma3` - Application directory containing docker-compose.yml
- `vllm_data` volume - Model cache directory (stores downloaded models)
- `open_webui_data` volume - Chat UI persistent data (chat history, settings)

## Service Communication

The UI service automatically connects to the API service running on `localhost:8000`. Both services run on the same instance and communicate over the Docker network.

## Hugging Face Authentication

Gemma 3 is a gated model requiring authentication through Hugging Face. During deployment, you must provide a Hugging Face API token. To get your free token, follow the below steps:

1. Create a free account at [huggingface.co/join](https://huggingface.co/join)
2. Accept the Gemma license at [huggingface.co/google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it)
3. Generate a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (Read-only access is sufficient)
4. Provide the token during deployment via UDF

The token is stored securely as an environment variable during deployment, and used only for model downloads from Hugging Face Hub.

## RAG Operations in Open WebUI

Open WebUI provides built-in support for RAG operations allowing users to chat with their documents. This implementation uses Nginx as a frontend web service proxy to the Open WebUI container. Users that are looking to upload documents larger than 100MBs are required to update Nginx's `client_max_body_size` to a larger value.

You can find the Nginx virtual host configuration in `/etc/nginx/sites-enabled/${DOMAIN}`. Where `${DOMAIN}` should reflect the rDNS of your compute instance.

## Service Communication

The UI service automatically connects to the API service running on `localhost:8000`. Both services run on the same instance and communicate over the Docker network.

## Resource Requirements

### For Gemma 3 4B
- **GPU**: Any supported Linode GPU instance type
- **Memory**: 16GB RAM or higher
- **Storage**: Sufficient space for model files (models can be several GB)
- **Reference**: [gemma-3-4b-it on Hugging Face](https://huggingface.co/google/gemma-3-4b-it)

### For Gemma 3 12B
- **GPU**: Any supported Linode GPU instance type
- **Memory**: 32GB RAM or higher
- **Storage**: Sufficient space for model files (models can be several GB)
- **Reference**: [gemma-3-12b-it on Hugging Face](https://huggingface.co/google/gemma-3-12b-it)

## RAG Operations in Open WebUI

Open WebUI provides built-in support for RAG operations allowing users to chat with their documents. This implementation uses Nginx as a frontend web service proxy to the Open WebUI container. Users that are looking to upload documents larger than 100MBs are required to update Nginx's `client_max_body_size` to a larger value.

You can find the Nginx virtual host configuration in `/etc/nginx/sites-enabled/${DOMAIN}`. Where `${DOMAIN}` should reflect the rDNS of your compute instance.