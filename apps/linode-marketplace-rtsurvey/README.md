# rtSurvey Linode Marketplace 1-Click App

rtSurvey is a professional-grade, self-hosted survey management and field data collection platform trusted by the World Bank, UNDP, ADB, and government agencies across Southeast Asia. Built on the open XLSForm standard, it supports 23+ question types, full offline mobile collection (Android/iOS), real-time R/Shiny analytics dashboards, enterprise SSO (Keycloak/Azure AD), and built-in data quality assurance tools.

## Software Included

| Software | Version | Description |
| :--- | :--- | :--- |
| rtSurvey | 1.0.0 | Self-hosted survey management and field data collection platform |
| Docker | Latest | Container runtime for all application services |
| Nginx | 1.18+ | Reverse proxy and SSL termination |
| MySQL | 8.0 | Relational database for survey data |
| Keycloak | Latest | SSO and identity management |
| Certbot | Latest | Automated SSL/TLS certificate management via Let's Encrypt |
| UFW | 0.36 | Firewall — allows HTTP, HTTPS, and SSH |

**Supported Distributions:**

- Ubuntu 22.04 LTS

## Use our API

Customers can choose to deploy rtSurvey through the Linode Marketplace or directly using the API. Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/).

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/ubuntu22.04",
    "region": "ap-southeast",
    "type": "g6-standard-2",
    "label": "rtsurvey-linode",
    "root_pass": "A_Really_Great_Password",
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 00000,
    "stackscript_data": {
        "sudo_username": "rtuser",
        "sudo_password": "A_Really_Great_Password",
        "ssh_public_key": "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer",
        "timezone": "Asia/Ho_Chi_Minh"
    }
}' https://api.linode.com/v4/linode/instances
```

CLI:
```
linode-cli linodes create \
  --image linode/ubuntu22.04 \
  --region ap-southeast \
  --type g6-standard-2 \
  --label rtsurvey-linode \
  --root_pass A_Really_Great_Password \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{"sudo_username":"rtuser","sudo_password":"A_Really_Great_Password","ssh_public_key":"ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer","timezone":"Asia/Ho_Chi_Minh"}'
```

## Resources

- [rtSurvey Documentation](https://docs.rtsurvey.com)
- [rtSurvey Support](https://docs.rtsurvey.com/contact/)
- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [StackScript Reference](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
