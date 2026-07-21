# Akamai Microsoft Agent Framework Quick Deploy App

Microsoft Agent Framework is an open-source framework for building, orchestrating, and deploying AI agents and multi-agent applications. It provides developers with the tools to create intelligent agents that can reason, use tools, collaborate, and automate complex workflows.

## Software Included

| Software  | Version           | Description                               |
| :---      | :----             | :---                                      |
| `agent-framework`  | `latest` | Microsoft Agent Framework Python library  |

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

Once your instance has finished provisioning you will be able to create your agents by importing `agent-framework` package into your project. You will be able to find an example application from Microsoft's documentation in the next section.


## Resource

- [Getting Started](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-python#get-started)