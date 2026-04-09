# rtSurvey — Deployment Guide

## Overview

rtSurvey is a self-hosted Smart Survey platform for field research, data collection, and CAPI (Computer-Assisted Personal Interviewing). It is built by RTA (rta.vn) and runs on Docker.

## Requirements

| Requirement | Value |
|-------------|-------|
| OS | Ubuntu 22.04 LTS |
| Recommended Plan | Dedicated 4 GB (4 CPU, 4 GB RAM) |
| Minimum Plan | Shared 4 GB |
| Disk | 80 GB SSD |

## Deployment Configuration

At deploy time, you will be asked for:

| Field | Description |
|-------|-------------|
| **Limited Sudo Username** | A non-root user that will be created with sudo privileges |
| **Limited Sudo Password** | Password for the sudo user |
| **SSH Public Key** | (Optional) Adds an SSH key for the sudo user |
| **Timezone** | Server timezone (default: `Asia/Ho_Chi_Minh`) |

All application passwords (database, admin, Keycloak) are generated automatically on the server.

## After Deployment

### 1. Get your credentials

SSH into your Linode as the sudo user you created:

```bash
ssh <sudo_username>@<your-linode-ip>
cat ~/.credentials
```

### 2. Log in to rtSurvey

Open `http://<your-linode-ip>` in a browser.

- Username: `admin`
- Password: (see `~/.credentials`)

### 3. Configure your domain and SSL

1. In the app, go to **Configuration → System Properties → Domain & SSL**
2. Enter your domain name (must already point to your Linode's IP via DNS)
3. Select SSL type:
   - **Let's Encrypt (certbot)** — recommended; issues a free TLS certificate automatically
   - **rtsurvey.com** — for *.rtsurvey.com subdomains
4. Click Save — the server will obtain a certificate and switch to HTTPS automatically

### 4. Keycloak SSO (pre-installed)

An embedded Keycloak instance is available at `https://<domain>/auth/admin` after SSL is active.

- Login: `admin` / (see `~/.credentials` → Keycloak Admin Password)

## Logs

| Log | Location |
|-----|----------|
| Deployment log | `/var/log/stackscript.log` |
| SSL trigger log | `/var/log/rtsurvey-ssl.log` |
| App files | `/opt/rtsurvey/` |

## Support

- Documentation: https://docs.rtsurvey.com
- Support: support+info@rta.vn
