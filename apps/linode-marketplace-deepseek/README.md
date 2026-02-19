# Akamai Cloud Compute - DeepSeek R1 and Open WebUI Deployment One-Click App

Open WebUI is an open-source, self-hosted web interface for interacting with and managing large language models. It supports multiple AI backends, multi-user access, and extensible integrations, enabling secure and customizable deployment for local or remote model inference.

Our Marketplace application deploys DeepSeek R1 distilled models (Qwen2.5-based) with vLLM as the inference backend and Open WebUI as the chat interface. These models are distilled from the full 671B DeepSeek-R1, providing enhanced chain-of-thought reasoning capabilities in smaller, deployable sizes.

During deployment, you can choose between three model sizes to match your GPU capabilities and performance requirements. See **Resource Requirements** below.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Docker    | `29.2.1`    | Container Management Runtime |
| Docker Compose    | `v5.0.2`    | Tool for multi-container applications |
| Nginx    | `1.24.0`    | HTTP server used to serve web applications |
| vLLM | `v0.14.0` | Library to run LLM inference models  |
| Open WebUI | `magin` tag | Self-hosted AI interface platform |

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
| GPU Utils | Detects GPU on the instance and install NVIDIA drivers | Writes `gpu_devices`, `gpu_count`, and `_has_gpu` to `group_vars/linode/vars` |

# Architecture

## Overview

The DeepSeek R1 deployment consists of two containerized services that work together to provide a complete AI inference stack:

1. **API Service** (`vLLM`): High-performance inference engine with tensor parallelism
2. **UI Service** (`Open WebUI`): Feature-rich chat interface

Both services are managed via Docker Compose and configured to restart automatically.

## Containerized Services

### API Service (vLLM)

- **Port**: `localhost:8000`
- **Container**: `vllm/vllm-openai:v0.14.0`
- **Model**: `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`, `14B`, or `32B` (user selectable)
- **Purpose**: High-performance inference engine with OpenAI-compatible REST API
- **Features**:
  - OpenAI-compatible REST API
  - GPU-accelerated inference with automatic tensor parallelism (required for 14B and 32B models)
  - MIT licensed models (no authentication required)
  - Chain-of-thought reasoning with `<think>` traces
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

- `/opt/deepseek` - Application directory containing docker-compose.yml
- `vllm_data` volume - Model cache directory (stores downloaded models)
- `open_webui_data` volume - Chat UI persistent data (chat history, settings)

## Service Communication

The UI service automatically connects to the API service running on `localhost:8000`. Both services run on the same instance and communicate over the Docker network.

## Tensor Parallelism

The deployment automatically detects the number of available GPUs and configures vLLM to use tensor parallelism across all of them. This is required for the 14B and 32B models (which do not fit on a single GPU).

## RAG Operations in Open WebUI

Open WebUI provides built-in support for RAG operations allowing users to chat with their documents. This implementation uses Nginx as a frontend web service proxy to the Open WebUI container. Users that are looking to upload documents larger than 100MBs are required to update Nginx's `client_max_body_size` to a larger value.

You can find the Nginx virtual host configuration in `/etc/nginx/sites-enabled/${DOMAIN}`. Where `${DOMAIN}` should reflect the rDNS of your compute instance.

## Resource Requirements

### For DeepSeek R1 Distill Qwen 7B
- **GPU**: Any 1-GPU instance (RTX 4000 Ada or Quadro RTX 6000)
- **RAM**: 16GB or higher
- **Storage**: Sufficient space for model files (~14GB download)
- **Compatible Plans**: All Ada 1-GPU plans, Quadro RTX 6000 1-GPU
- **Reference**: [DeepSeek-R1-Distill-Qwen-7B on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B)

### For DeepSeek R1 Distill Qwen 14B
- **GPU**: Any 2-GPU instance or higher (RTX 4000 Ada or Quadro RTX 6000)
- **RAM**: 32GB or higher
- **Storage**: Sufficient space for model files (~28GB download)
- **Compatible Plans**: All Ada 2-GPU and 4-GPU plans, Quadro RTX 6000 2-GPU, 3-GPU, and 4-GPU
- **Reference**: [DeepSeek-R1-Distill-Qwen-14B on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B)

### For DeepSeek R1 Distill Qwen 32B
- **GPU**: Any 4-GPU instance (RTX 4000 Ada or Quadro RTX 6000)
- **RAM**: 128GB or higher
- **Storage**: Sufficient space for model files (~64GB download)
- **Compatible Plans**: Ada 4-GPU plans, Quadro RTX 6000 4-GPU
- **Reference**: [DeepSeek-R1-Distill-Qwen-32B on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B)
