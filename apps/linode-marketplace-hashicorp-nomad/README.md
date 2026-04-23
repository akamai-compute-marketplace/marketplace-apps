# Linode HashiCorp Nomad One-Click App

Deploy a production-ready single-node HashiCorp Nomad Community Edition installation. This One-Click App installs Nomad CE from HashiCorp's official apt repository, running as a combined server and client on one VM with ACLs enabled and the API bound to loopback. An NGINX reverse proxy with a Let's Encrypt SSL certificate and HTTP basic authentication sits in front of the Nomad UI, so access requires two credentials: an NGINX basic-auth password (set during deployment) and a Nomad ACL management token (generated on first boot and written to the sudo user's credentials file).

## Software Included

| Software | Version | Description |
| :--- | :--- | :--- |
| HashiCorp Nomad | Latest (Community Edition) | Workload orchestrator running as combined server and client on a single node, with ACLs enabled. |
| NGINX | 1.24.0 | Reverse proxy handling SSL termination and HTTP basic authentication for the Nomad UI. |

**Supported Distributions:**
- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | The UFW module installs and enables UFW, then opens only ports 22, 80, and 443. The Nomad HTTP (4646), RPC (4647), and Serf (4648) ports are never exposed publicly; they are reachable only via the nginx reverse proxy on the same host. |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |
| Create DNS Record | The Create DNS Record module creates DNS records for domains and subdomains using the Linode API, including validation of DNS propagation. |
| Secure SSH | The Secure SSH module configures SSH security settings including disabling root login and password authentication when appropriate. |
| SSH Key | The SSH Key module manages SSH key deployment for the sudo user, supporting both custom public keys and account keys. |
| Certbot SSL | The Certbot SSL module handles SSL/TLS certificate installation via Let's Encrypt, supporting Nginx certificate issuance. |

## Accessing the Nomad UI

After deployment, open `https://<your-domain-or-rDNS>/` in a browser. Access is gated by two layers:

1. **NGINX HTTP Basic Authentication.** Your browser will prompt for a username and password on the first request. The credentials are written to `/home/<sudo-user>/.credentials` on the Linode; the username defaults to `nomad` and the password is randomly generated at deploy time.
2. **Nomad ACL sign-in.** Once past basic auth, navigate to `/ui/signin` and paste the management token (the `Secret ID`) from `.credentials` into the sign-in form. The Nomad UI treats the "Anonymous Token" as an active session, so on first sign-in you may need to click **Sign Out** on the profile page before the sign-in form accepts a new token.

The Nomad CLI can connect to the server over the same endpoint:

```bash
export NOMAD_ADDR=https://<your-domain-or-rDNS>
export NOMAD_TOKEN=<Secret ID from .credentials>
export NOMAD_HTTP_AUTH=<htpasswd-user>:<htpasswd-password>
nomad node status
```

## Use our API

Customers can choose to deploy HashiCorp Nomad through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Make sure that the following values are updated at the top of the code block before running the commands:
- `TOKEN` (Your Linode API Token)
- `ROOT_PASS` (Secure password for the root user)

### cURL

```bash
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu24.04",
    "private_ip": true,
    "region": "us-east",
    "stackscript_data": {
        "user_name": "admin",
        "disable_root": "Yes",
        "token_password": "$TOKEN",
        "subdomain": "www",
        "domain": "example.com",
        "soa_email_address": "admin@example.com",
        "nomad_htpasswd_user": "nomad",
        "add_ons": "none"
    },
    "stackscript_id": [STACKSCRIPT_ID],
    "type": "g6-standard-2",
    "label": "hashicorp-nomad",
    "tags": [
        "hashicorp-nomad"
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
  --image 'linode/ubuntu24.04' \
  --private_ip true \
  --region us-east \
  --stackscript_data '{"user_name":"admin","disable_root":"Yes","token_password":"$TOKEN","subdomain":"www","domain":"example.com","soa_email_address":"admin@example.com","nomad_htpasswd_user":"nomad","add_ons":"none"}' \
  --stackscript_id [STACKSCRIPT_ID] \
  --type g6-standard-2 \
  --label hashicorp-nomad \
  --tags hashicorp-nomad \
  --root_pass '$ROOT_PASSWORD' \
  --authorized_users your_ssh_user \
  --disk_encryption disabled
```

## Resources

- [HashiCorp Nomad Documentation](https://developer.hashicorp.com/nomad/docs)
- [Marketplace App Documentation](https://www.linode.com/docs/marketplace-docs/guides/hashicorp-nomad/)
- [Nomad ACL System Overview](https://developer.hashicorp.com/nomad/docs/secure/acl)
- [Configure a web UI reverse proxy](https://developer.hashicorp.com/nomad/docs/deploy/clusters/reverse-proxy-ui)
