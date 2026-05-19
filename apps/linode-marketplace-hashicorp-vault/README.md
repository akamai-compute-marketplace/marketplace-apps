# Linode HashiCorp Vault One-Click App

Deploy a single-node HashiCorp Vault Community Edition installation with secure defaults. This One-Click App installs Vault CE from HashiCorp's official apt repository, using integrated raft storage. An NGINX reverse proxy with a Let's Encrypt SSL certificate sits in front of Vault on ports 80 and 443. Vault is automatically initialized and unsealed during deployment, so the operator only needs the root token (written to the sudo user's credentials file) to sign in via the UI.

## Software Included

| Software | Version | Description |
| :--- | :--- | :--- |
| HashiCorp Vault | Latest (Community Edition) | Secrets management and data encryption. |
| NGINX | 1.24.0 | Web server and reverse proxy with Let's Encrypt SSL termination. |

**Supported Distributions:**
- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | The Hostname module uses `dnsdomainname -A` to detect the Linode's FQDN and write to the `/etc/hosts` file. This defaults to the Linode's automatically assigned rDNS. To use a custom FQDN see [Configure your Linode for Reverse DNS](https://www.linode.com/docs/guides/configure-your-linode-for-reverse-dns/).  |
| Update Packages   | The Update Packages module performs apt update and upgrade actions as root.  |
| UFW   | The UFW module installs and enables UFW, then opens only ports 22, 80, and 443. Vault's API (8200) and cluster (8201) ports are never exposed publicly; both are bound to `127.0.0.1` and reachable only via the nginx reverse proxy on the same host. |
| Fail2Ban   | The Fail2Ban module installs, activates and enables the Fail2Ban service.  |
| Create DNS Record | The Create DNS Record module creates DNS records for domains and subdomains using the Linode API, including validation of DNS propagation. |
| Secure SSH | The Secure SSH module configures SSH security settings including disabling root login and password authentication when appropriate. |
| SSH Key | The SSH Key module manages SSH key deployment for the sudo user, supporting both custom public keys and account keys. |
| Certbot SSL | The Certbot SSL module handles SSL/TLS certificate installation via Let's Encrypt, supporting Nginx certificate issuance. |

## Accessing the Vault UI

After deployment, open `https://<your-domain-or-rDNS>/` in a browser. Vault redirects to `/ui/vault/auth`. Sign in with method **Token** and paste the value of `Initial Root Token` from `/home/<user>/.credentials`.

### Vault unseal keys

The deploy auto-initializes Vault and unseals it with 3 of the 5 generated keys. So on the first login, all you need to provide is the root token. The 5 unseal keys remain in the credentials file because Vault is sealed by design every time the `vault` systemd unit restarts. When that happens, the UI redirects to `/ui/vault/unseal`. If this happens, paste 3 of the 5 keys to unseal, then sign in with the root token as usual.

**Security note.** Storing all 5 unseal keys and the root token in a single file is for convenience only, and not recommended for production. Therefore, it is recommended to:

1. Distribute the 5 unseal keys to 5 separate trusted operators. Do not retain a local copy.
2. Generate a new root token, then revoke the initial one.
3. Securely delete `/home/<user>/.credentials` once the keys are distributed.

## Deployment Topology

Vault runs as a single node using integrated raft storage. One Vault process serves both the API surface on `127.0.0.1:8200` (HTTPS, using the postinst self-signed cert) and the raft cluster listener on `127.0.0.1:8201`. NGINX terminates the external Let's Encrypt-issued TLS on port 443 and proxies to Vault's loopback HTTPS listener. The proxy hop is encrypted but skips cert verification because the cert is the postinst self-signed pair.

This topology is sufficient for small workloads, dev/staging, and learning. To scale to high-availability later, deploy additional Linodes, set each node's `api_addr` to its own externally-reachable URL and `cluster_addr` to an inter-cluster-reachable URL, then run `vault operator raft join` to add peers. Multi-node HA is out of scope for this One-Click App.

## Use our API

Customers can choose to deploy HashiCorp Vault through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

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
        "add_ons": "none"
    },
    "stackscript_id": [STACKSCRIPT_ID],
    "type": "g6-standard-2",
    "label": "hashicorp-vault",
    "tags": [
        "hashicorp-vault"
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
  --stackscript_data '{"user_name":"admin","disable_root":"Yes","token_password":"$TOKEN","subdomain":"www","domain":"example.com","soa_email_address":"admin@example.com","add_ons":"none"}' \
  --stackscript_id [STACKSCRIPT_ID] \
  --type g6-standard-2 \
  --label hashicorp-vault \
  --tags hashicorp-vault \
  --root_pass '$ROOT_PASSWORD' \
  --authorized_users your_ssh_user \
  --disk_encryption disabled
```

## Resources

- [HashiCorp Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault Production Hardening](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)
- [Marketplace App Documentation](https://www.linode.com/docs/marketplace-docs/guides/hashicorp-vault/)
- [Vault Integrated Storage (Raft) Overview](https://developer.hashicorp.com/vault/docs/configuration/storage/raft)
