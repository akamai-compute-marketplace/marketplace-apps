# Akamai Cloud Compute - Ollama and Open WebUI Deployment One-Click App

Open WebUI is an open-source, self-hosted web interface for interacting with and managing large language models. It supports multiple AI backends, multi-user access, and extensible integrations, enabling secure and customizable deployment for local or remote model inference.

Our Quick Deploy application sets up Ollama as the inference backend paired with Open WebUI as the chat interface. Ollama makes it simple to pull and run a wide range of open-source large language models locally, with full GPU acceleration and no external API dependencies required.

During deployment, you can choose between three model sizes to match your GPU capabilities and performance requirements. See **Resource Requirements** below.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Docker    | `29.4.0`    | Container Management Runtime |
| Docker Compose    | `v5.0.2`    | Tool for multi-container applications |
| Nginx    | `1.24.0`    | HTTP server used to serve web applications |
| Ollama | `latest` | Local LLM inference engine with GPU support |
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
| GPU Utils | Detects GPU on the instance and install NVIDIA drivers | Writes `gpu_devices`, `gpu_count`, and `_has_gpu` to `group_vars/linode/vars` |

# Architecture

### Overview

The deployment consists of two containerized services that work together to provide a complete AI inference stack:

1. **Ollama**: Local LLM inference engine with GPU acceleration
2. **Open WebUI**: Feature-rich browser-based chat interface

Both services are managed via Docker Compose and configured to restart automatically (`unless-stopped`).

---

## Containerized Services

### Ollama (LLM Engine)

- **Port**: `localhost:11434`
- **Container**: `ollama/ollama:latest`
- **Purpose**: Local inference engine with a REST API compatible with OpenAI-style clients
- **Features**:
  - GPU-accelerated inference using all available NVIDIA GPUs
  - Supports a wide range of open models (Llama, Mistral, Gemma, Qwen, DeepSeek, etc.)
  - Model persistence via Docker volume
  - Health check via `ollama list`

### Open WebUI (Chat Interface)

- **Port**: `localhost:3000`
- **Container**: `ghcr.io/open-webui/open-webui:main`
- **Purpose**: Browser-based chat interface connected to Ollama
- **Features**:
  - Browser-based chat UI
  - Persistent chat history
  - Automatically connects to Ollama at `http://ollama:11434`
  - Multi-user support
  - Telemetry disabled by default (`ANONYMIZED_TELEMETRY=false`)

---

## Directory Structure

The following Docker volumes are used:

- `ollama_data` — Stores downloaded models and Ollama configuration (`/root/.ollama`)
- `open_webui_data` — Stores chat history, user settings, and UI data (`/app/backend/data`)

---

## Service Communication

Open WebUI connects to Ollama over the internal Docker network using the service name as the hostname (`http://ollama:11434`). Both services run on the same host and communicate without exposing Ollama publicly.

---

## Adding New Models

To pull and run a new model, use `docker exec` to interact with the running Ollama container.

### Pull a model

```bash
docker exec ollama ollama pull 
```

**Examples:**

```bash
# Pull Llama 3.2 (3B)
docker exec ollama ollama pull llama3.2

# Pull Mistral 7B
docker exec ollama ollama pull mistral

# Pull DeepSeek R1 (7B)
docker exec ollama ollama pull deepseek-r1:7b

# Pull Gemma 3 (4B)
docker exec ollama ollama pull gemma3:4b

# Pull Qwen 2.5 (7B)
docker exec ollama ollama pull qwen2.5:7b
```

Browse the full model library at [ollama.com/library](https://ollama.com/library).

### List downloaded models

```bash
docker exec ollama ollama list
```

### Remove a model

```bash
docker exec ollama ollama rm 
```

### Run a model directly in the terminal (optional)

```bash
docker exec -it ollama ollama run 
```

Once pulled, models will automatically appear in the Open WebUI model selector — no restart required.

---

## Resource Requirements

GPU resources are reserved automatically for all available NVIDIA devices. Requirements will vary depending on the model you choose to run.

| Model Size | VRAM Required | Example Models |
| :--- | :--- | :--- |
| 3B–7B | 6–8GB VRAM | Llama 3.2 3B, Mistral 7B, DeepSeek R1 7B |
| 8B–14B | 10–16GB VRAM | Llama 3.1 8B, DeepSeek R1 14B, Gemma 3 12B |
| 32B+ | 24GB+ VRAM | DeepSeek R1 32B, Qwen 2.5 32B |

For multi-GPU setups, Ollama will automatically use all available GPUs as configured in the Compose file (`count: all`).Sonnet 4.6Claude is AI and can make mistakes. Please double-