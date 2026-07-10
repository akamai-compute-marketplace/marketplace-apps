# Linode HaltDOS Community WAF One-Click App

Deploy a single-node [HaltDOS Community WAF](https://docs.haltdos.com/community/introduction/). The app installs HaltDOS Community Edition's two services — `hd-community-waf` (the offloader, a WAF data plane) and `hd-community-controller` (the management UI) — from HaltDOS's official apt repository. NGINX fronts the management UI with a Let's Encrypt certificate and HTTP basic authentication on the setup wizard endpoints.

## Software Included

| Software | Version | Description |
| :--- | :--- | :--- |
| HaltDOS Community WAF (`hd-community-waf`) | 1.0.4 | OpenResty/nginx-based WAF data plane that inspects and filters HTTP traffic. |
| HaltDOS Community Controller (`hd-community-controller`) | 1.0.5 | Spring Boot management UI for configuring listeners and rules. |
| NGINX | 1.18.0 | Web server and reverse proxy for the management UI. |

**Supported Distributions:**
- Ubuntu 22.04 LTS

## Linode Helpers Included

| Name | Action |
| :--- | :--- |
| Hostname | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN. Defaults to the Linode's automatically assigned rDNS. To use a custom FQDN, see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/). |
| Update Packages | Performs apt update and upgrade actions as root. |
| UFW | Installs and enables UFW. Opens ports 22 (SSH), 80 and 443 (reserved for the WAF data plane once you configure your first listener; port 80 also handles Let's Encrypt issuance), and 9000 (management UI). |
| Fail2Ban | Installs, activates, and enables Fail2Ban. |
| Create DNS Record | Creates DNS A records via the Linode API when a domain and API token are supplied. |
| Secure SSH | Configures SSH security settings, including disabling root login when requested. |
| SSH Key | Manages SSH key deployment for the sudo user. |
| Certbot SSL | Issues a Let's Encrypt certificate for the management UI hostname (rDNS by default). |

## Accessing the Management UI

After deployment, open `https://<your-domain-or-rDNS>:9000/setup` in a browser. Two-step credential flow:

1. **NGINX HTTP Basic Authentication.** Your browser prompts for a username and password on the first request to the wizard. Username is `haltdos`; password is randomly generated and written to `/home/<user>/.credentials` on the Linode.
2. **HaltDOS wizard.** Complete three steps:
   - **User Registration** — full name, email, organization, designation, country, phone.
   - **Account Details** — admin username and password for the controller.
   - **OTP Verification** — a six-digit code emailed to the address you entered in step 1. The OTP is generated and sent by HaltDOS's hosted licensing service at `community.haltdos.com`; if it does not arrive within 10 minutes, contact `support@haltdos.com`.

Once the wizard is complete, `/setup` redirects to the login page. Sign in with the admin username and password you set in step 2.

## Starting the WAF Data Plane

The offloader ships **disabled** on first deploy. Do not enable or start it until you have configured at least one listener in the management GUI.

> **Security note.** If the offloader is started without a configured listener, its default-server fallback exposes the data-plane working directory (`/root`) over plain HTTP on port 80. The marketplace app explicitly disables the unit at install time so this cannot happen accidentally on a fresh deploy or after a reboot. Only enable the unit once you have a listener configured.

After you have created at least one listener in the management GUI:

```bash
sudo systemctl enable --now offloader
```

This both enables auto-start on subsequent reboots and starts the unit now. The offloader then binds 80 and 443 and inspects traffic for the listeners you have configured. UFW already permits both ports.

## Architecture

```
                         ┌─ Linode (single VM) ────────────────────────┐
                         │                                             │
                         │   ┌─────────┐         ┌──────────────────┐  │
  Operator               │   │  NGINX  │ proxy   │   CONTROLLER     │  │
  ─── HTTPS :9000 ──────►│   │  SSL +  │────────►│  127.0.0.1:9001  │  │
                         │   │  auth   │         │  (loopback only) │  │
                         │   └─────────┘         └──────────────────┘  │
                         │                                             │
                         │   ┌──────────────┐                          │
  End user / attacker    │   │   OFFLOADER  │  ──►  Your protected     │
  ─── HTTP/HTTPS         │   │  (WAF data   │       upstream app(s)    │
       :80, :443  ───────┼──►│    plane)    │       (configure in UI)  │
                         │   └──────────────┘                          │
                         │                                             │
                         └─────────────────────────────────────────────┘
```

- **Controller** (Spring Boot WAR, management UI) binds to `127.0.0.1:9001` and is **not** reachable directly from outside the host.
- **NGINX** terminates SSL on port 9000 with a Let's Encrypt certificate and reverse-proxies to the controller. The setup wizard endpoints (`/setup`, `/api/register`, `/api/setup`) are gated by HTTP basic authentication; everything else relies on the controller's native authentication.
- **Offloader** (the WAF data plane) ships **disabled** on first deploy. It binds 80/443 once started, to inspect and forward traffic destined for the upstream apps you protect via the management GUI. The unit is intentionally disabled at install time because starting it without a configured listener exposes the data-plane working directory (`/root`) via plain HTTP on port 80. After you create your first listener, run `sudo systemctl enable --now offloader` to enable it (so it auto-starts on subsequent reboots) and start it immediately.

## Deployment Topology

This One-Click App deploys both the controller (management plane) and the offloader (data plane) on the same Linode. Suitable for small workloads, dev/staging, and learning. For production scale-out, refer to the [HaltDOS Community Edition Overview](https://docs.haltdos.com/community/docs/overview/).

## Use our API

You can deploy HaltDOS through the Linode Marketplace or directly via API. Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/).

Update these values at the top of the snippet:
- `TOKEN` — your Linode API Token
- `ROOT_PASS` — secure password for the root user

The `domain` and `subdomain` fields can be left empty — when omitted, the deploy issues the Let's Encrypt certificate against the Linode's automatically assigned rDNS hostname.

### cURL

```bash
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu22.04",
    "private_ip": true,
    "region": "us-east",
    "stackscript_data": {
        "user_name": "admin",
        "disable_root": "Yes",
        "token_password": "$TOKEN",
        "subdomain": "www",
        "domain": "example.com",
        "soa_email_address": "admin@example.com",
        "add_ons": "none"
    },
    "stackscript_id": [STACKSCRIPT_ID],
    "type": "g6-standard-2",
    "label": "haltdos",
    "tags": [
        "haltdos"
    ],
    "root_pass": "$ROOT_PASSWORD",
    "authorized_users": [
        "your_ssh_user"
    ],
    "disk_encryption": "disabled"
}' https://api.linode.com/v4/linode/instances
```

### Linode CLI

```bash
linode-cli linodes create \
  --image 'linode/ubuntu22.04' \
  --private_ip true \
  --region us-east \
  --stackscript_data '{"user_name":"admin","disable_root":"Yes","token_password":"$TOKEN","subdomain":"www","domain":"example.com","soa_email_address":"admin@example.com","add_ons":"none"}' \
  --stackscript_id [STACKSCRIPT_ID] \
  --type g6-standard-2 \
  --label haltdos \
  --tags haltdos \
  --root_pass '$ROOT_PASSWORD' \
  --authorized_users your_ssh_user \
  --disk_encryption disabled
```

## Resources

- [HaltDOS Community Edition Documentation](https://docs.haltdos.com/community/)
- [HaltDOS Installation Prerequisites](https://docs.haltdos.com/community/getting-started/pre-requisites/)
- [Marketplace App Documentation](https://www.linode.com/docs/marketplace-docs/guides/haltdos-community-waf/)
- HaltDOS support contact for OTP / licensing issues: `support@haltdos.com`
