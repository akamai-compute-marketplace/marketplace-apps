# Defensia Security Agent

## Introduction

[Defensia](https://defensia.cloud) is a lightweight security monitoring agent for Linux servers. It detects and blocks real-time threats including SSH brute force attacks, web application attacks, and suspicious traffic patterns — all visible from a central dashboard.

## Software Included

| Software | Version | Description |
|----------|---------|-------------|
| defensia-agent | latest | Real-time security monitoring daemon |

## Supported Distributions

- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS

## Linode Helpers Included

- **Hostname** — configures the system hostname
- **Update Packages** — ensures all system packages are up to date
- **UFW** — enables the Uncomplicated Firewall
- **Fail2Ban** — provides additional brute force protection

## Features

- **SSH attack detection** — monitors auth logs and blocks brute force attempts in real time
- **Web attack detection** — detects SQLi, XSS, path traversal, RCE attempts in web server logs
- **IP blocking** — automatically bans attacking IPs via iptables
- **Central dashboard** — view all your servers and events at [defensia.cloud](https://defensia.cloud)
- **WAF** — Web Application Firewall with per-agent configuration
- **Bot detection** — fingerprints and scores crawler and bot traffic

## Deployment

### Required UDF Fields

| Field | Description |
|-------|-------------|
| `token` | Your Defensia install token — generate one at https://defensia.cloud → Add Server |
| `agent_name` | Name for this server in your dashboard (defaults to hostname if left blank) |

### Using the Linode CLI

```bash
linode-cli linodes create \
  --type g6-nanode-1 \
  --region us-ord \
  --image linode/ubuntu24.04 \
  --root_pass <your-root-password> \
  --label my-defensia-server \
  --stackscript_id <stackscript-id> \
  --stackscript_data '{"token":"<your-token>","agent_name":"my-server"}'
```

## Resources

- [Defensia Documentation](https://defensia.cloud/docs)
- [Akamai Compute Marketplace](https://www.linode.com/marketplace/)
- [Report Issues](https://github.com/defensia/agent/issues)
