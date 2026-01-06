# Linode Milvus One-Click App

Deploy a production-ready instance of Milvus, the open-source vector database built for AI, embeddings, and similarity search. Ideal for powering retrieval-augmented generation (RAG), semantic search, and AI application backends.

## Software Included

| Software     | Version            | Description                                 |
| :----------- | :----------------- | :------------------------------------------ |
| Milvus | Latest | Open-source vector database for AI and similarity search      |
| Docker | Latest | Container Management tool      |
| Nginx | Latest | HTTP server used to serve web applications |
  

**Supported Distributions:**
- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname         | Uses `dnsdomainname -A` to detect and write the Linode's FQDN to `/etc hosts`.                                            |
| Update Packages  | Performs `apt update` and `apt upgrade` as root.                                                                           |
| UFW              | Configures firewall rules and enables the service.                                                                         |
| Fail2Ban         | Installs and enables Fail2Ban to monitor and block malicious login attempts.                                               |
| Create DNS Record| Uses the Linode API to create DNS records for the specified domain/subdomain.                                             |
| Secure SSH       | Hardens SSH settings including disabling root login and password-based authentication.                                    |
| SSH Key          | Deploys custom or account SSH keys for secure access.                                                                      |

## Use our API

Customers can choose to deploy Milvus via the Linode Marketplace or through the API directly. Before using the commands below, generate an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/).

Make sure to update the following values before running the commands:
- `TOKEN` - Your Linode API token  
- `ROOT_PASS` - Root password for the Linode  
- `USERNAME` - System user that will be created  
- `SOA_EMAIL_ADDRESS` - Email address for DNS & SSL  
- `DOMAIN` - Domain name (optional)  
- `SUBDOMAIN` - Subdomain for Cribl access (optional)

### SHELL:

```bash
export TOKEN="YOUR_API_TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="logs"

curl -H "Content-Type: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
-X POST -d '{
  "authorized_users": [
    "user1",
    "user2"
  ],
  "backups_enabled": true,
  "booted": true,
  "image": "linode/ubuntu24.04",
  "label": "milvus-server",
  "private_ip": true,
  "region": "us-southeast",
  "root_pass": "'"${ROOT_PASS}"'",
  "stackscript_data": {
    "user_name": "'"${USERNAME}"'",
    "disable_root": "Yes",
    "token_password": "'"${TOKEN}"'",
    "subdomain": "'"${SUBDOMAIN}"'",
    "domain": "'"${DOMAIN}"'",
    "soa_email_address": "'"${SOA_EMAIL_ADDRESS}"'"
  },
  "stackscript_id": 00000000000,
  "type": "g6-nanode-1",
  "tags": ["milvus"],
  "disk_encryption": "disabled"
}' https://api.linode.com/v4/linode/instances

CLI:
export TOKEN="YOUR_API_TOKEN"
export ROOT_PASS="aComplexP@ssword"
export USERNAME="user1"
export SOA_EMAIL_ADDRESS="user@example.com"
export DOMAIN="example.com"
export SUBDOMAIN="logs"

linode-cli linodes create \
--image 'linode/ubuntu24.04' \
--private_ip true \
--label milvus-server \
--root_pass ${ROOT_PASS} \
--booted true \
--stackscript_id 00000000000 \
--stackscript_data '{
  "user_name": "'"${USERNAME}"'",
  "disable_root": "Yes",
  "token_password": "'"${TOKEN}"'",
  "subdomain": "'"${SUBDOMAIN}"'",
  "domain": "'"${DOMAIN}"'",
  "soa_email_address": "'"${SOA_EMAIL_ADDRESS}"'"
}' \
--region us-east \
--type g6-nanode-1 \
--tags milvus \
--authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer" \
--authorized_users "user1" \
--authorized_users "user2" \
--disk_encryption disabled

```

## Resources
- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript reference](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
- [Milvus Documentation](https://milvus.io/docs)