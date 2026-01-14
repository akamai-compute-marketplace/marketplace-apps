# Akamai Cloud Compute - Gemma 3 and Open WebUI Deployment One-Click APP

Open WebUI is an open-source, self-hosted web interface for interacting with and managing large language models. It supports multiple AI backends, multi-user access, and extensible integrations, enabling secure and customizable deployment for local or remote model inference.

Our Marketplace application deploys Google Gemma 3, a state-of-the-art open-source large language model with multimodal understanding and multilingual capabilities. Built from the same technology that powers Google's Gemini models, Gemma 3 is optimized for instruction following, reasoning, and conversational tasks while maintaining efficient inference performance.

During deployment, you can choose between two model sizes to match your GPU capabilities and performance requirements.

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
| GPU Utils| Detects GPU on the instance and install NVIDIA drivers | Writes `gpu_device` and `_has_gpu` to `group_vars/linode/vars` |

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

Gemma 3 is a gated model requiring authentication through Hugging Face. During deployment, you must provide a Hugging Face API token:

1. Create a free account at [huggingface.co/join](https://huggingface.co/join)
2. Accept the Gemma license at [huggingface.co/google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it)
3. Generate a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (Read-only access is sufficient)
4. Provide the token during deployment via UDF

The token is stored securely as an environment variable and used only for model downloads from Hugging Face Hub.

## Model Selection

During deployment, you can choose between two Gemma 3 model sizes via the deployment form:

### Gemma 3 4B (Default - Recommended)
- **Parameters**: 4 billion
- **GPU Memory Required**: Minimum 12GB VRAM
- **Recommended GPU**: RTX 4000 Ada (20GB) or higher
- **VRAM Usage**: ~8.6GB
- **Performance**: Fast inference, excellent for most use cases
- **Use Cases**: General chat, coding assistance, document analysis, conversational AI

### Gemma 3 12B (Advanced)
- **Parameters**: 12 billion
- **GPU Memory Required**: Minimum 24GB VRAM
- **Recommended GPU**: RTX 6000 Ada (48GB), L40S (48GB), or higher
- **VRAM Usage**: ~20GB
- **Performance**: Higher quality responses, better reasoning capabilities
- **Use Cases**: Complex reasoning, advanced analysis, specialized tasks requiring maximum model capability
- **Important**: This model will NOT work on GPUs with less than 24GB VRAM (e.g., RTX 4000 Ada with 20GB)

## Resource Requirements

### For Gemma 3 4B
- **GPU**: NVIDIA RTX 4000 Ada (20GB) or higher
- **GPU Memory**: Minimum 12GB VRAM
- **System Memory**: 16GB+ RAM recommended
- **Storage**: 30GB+ for model files and cached data

### For Gemma 3 12B
- **GPU**: NVIDIA RTX 6000 Ada (48GB), L40S (48GB), or higher
- **GPU Memory**: Minimum 24GB VRAM (strictly required)
- **System Memory**: 32GB+ RAM recommended
- **Storage**: 50GB+ for model files and cached data

## Model Specifications

Both models share the following characteristics:

- **Type**: Instruction-tuned, text generation
- **Context Length**: 16,384 tokens
- **License**: Google Gemma Terms of Use
- **Capabilities**: Text generation, conversational AI, instruction following, reasoning tasks
- **Architecture**: Built from the same technology that powers Google's Gemini models

## RAG Operations in Open WebUI

Open WebUI provides built-in support for RAG operations allowing users to chat with their documents. This implementation uses Nginx as a frontend web service proxy to the Open WebUI container. Users that are looking to upload documents larger than 100MBs are required to update Nginx's `client_max_body_size` to a larger value.

You can find the Nginx virtual host configuration in `/etc/nginx/sites-enabled/${DOMAIN}`. Where `${DOMAIN}` should reflect the rDNS of your compute instance.

## Post-Deployment Notes

### First Startup
The initial container startup will download the selected Gemma 3 model from Hugging Face:
- **4B Model**: ~9GB download, typically 3-5 minutes
- **12B Model**: ~24GB download, typically 5-10 minutes

Download time depends on network speed. Subsequent startups use the cached model and start in 1-2 minutes.

### Accessing Credentials
After deployment, login credentials are available at:
```
/home/<username>/.credentials
```

### Monitoring GPU Usage
To monitor GPU utilization:
```bash
nvidia-smi
# or for real-time monitoring
watch -n 1 nvidia-smi
```

### Viewing Logs
```bash
# vLLM inference engine logs
docker logs vllm

# Open WebUI logs
docker logs open-webui
```

### Switching Models After Deployment

If you need to switch between the 4B and 12B models after deployment:

1. Edit the docker-compose configuration:
   ```bash
   nano /opt/gemma3/docker-compose.yml
   ```

2. Change the model in the vLLM command section:
   ```yaml
   command:
     - --model=google/gemma-3-4b-it    # or google/gemma-3-12b-it
   ```

3. Restart the containers:
   ```bash
   cd /opt/gemma3
   docker-compose restart
   ```

**Note**: When switching to the 12B model, ensure your GPU has at least 24GB VRAM or the container will fail to start with an out-of-memory error.
