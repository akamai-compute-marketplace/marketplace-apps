# Linode Haystack Quick Deploy App

Haystack is an open-source framework for building applications that use large language models (LLMs). Instead of requiring developers to write custom orchestration logic for every use case, it provides a structured way to assemble AI functionality through reusable components connected in pipelines. This approach makes it well suited for creating retrieval-augmented generation (RAG) systems, AI agents, search experiences, chat applications, and other LLM-driven solutions.

## Software Included

| Software  | Version       | Description               |
| :---      | :----         | :---                      |
| Haystack  | `latest`      | Haystack Python library   |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname | Assigns a hostname to the Linode based on the domain provided via UDF, or uses the default rDNS. For consistency, DNS and SSL configurations use the Hostname-generated `_domain` var. |
| Sudo User | Creates a limited `sudo` user from the UDF-supplied `username` and generates its password. Usernames containing illegal characters will cause the play to fail. |
| SSH Key | Writes a UDF-supplied SSH pubkey to `/home/$username/.ssh/authorized_keys`. To add an SSH key to `root`, use [Cloud Manager SSH Keys](https://www.linode.com/docs/products/tools/cloud-manager/guides/manage-ssh-keys/). |
| Secure SSH | Standard SSH hardening — writes to `/etc/ssh/sshd_config` to disable password auth and require public-key auth (applied only when `disable_root` is set). |
| Update Packages | Performs standard apt update and upgrade actions as root. |
| UFW | Imports `ufw_rules.yml` (22, 80, 443) and enables the firewall. PostgreSQL (5432) is not exposed. |
| Fail2Ban | Installs, activates, and enables the Fail2Ban service. |

## Deployment Details

Once your instance has finished provisioning you will be able to create your Haystack agents by importing `haystack-ai` package into your project. You will be able to find an example application from Haystack's documentation below:

- https://docs.haystack.deepset.ai/docs/get-started#build-your-first-agent

## Resource

- [Getting Started](https://docs.haystack.deepset.ai/docs/get-started)
- [Installation](https://docs.haystack.deepset.ai/docs/installation)
