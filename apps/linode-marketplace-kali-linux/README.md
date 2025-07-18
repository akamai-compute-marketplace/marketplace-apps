# Linode Kali Linux Deployment One-Click APP

This Marketplace app deploys Kali Linux on Ubuntu 24.04 LTS with optional VNC remote desktop access. Kali Linux is a specialized Linux distribution designed for penetration testing and security auditing.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Kali Linux Repository | kali-rolling | Official Kali Linux repository with rolling updates |
| Kali Linux Packages | latest | Configurable package selection (Everything, Default, or Core) |
| TigerVNC Server | latest | VNC server for remote desktop access (optional) |
| XFCE Desktop | latest | Lightweight desktop environment (when VNC is enabled) |
| LightDM | latest | Display manager (when VNC is enabled) |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Kali Linux Package Options

| Package  | Size | Description |
| :---     | :--- | :---        |
| Everything | 34GB | Complete Kali Linux installation with all tools (kali-linux-everything) |
| Default | 13GB | Standard Kali Linux installation (kali-linux-default) |
| Core | 1.5GB | Minimal Kali Linux installation with essential tools (kali-linux-core) |

## Linode Helpers Included

| Name  | Action  |
| :---  | :---    |
| Hostname   | Sets up the system hostname based on domain information. Uses the provided domain/subdomain or falls back to the Linode's default rDNS. |
| Update Packages   | Performs system package updates and upgrades using apt. |
| UFW   | Configures and enables UFW firewall with standard ports (SSH, HTTP, HTTPS). Additional ports can be configured in the application's UFW rules. |
| Fail2Ban   | Installs and configures Fail2Ban for protection against brute force attempts. |

## Use our API

Customers can choose to deploy the Kali Linux app through the Linode Marketplace or directly using API. Before using the commands below, you will need to create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token) or configure [linode-cli](https://www.linode.com/products/cli/) on an environment.

Update these values before running the commands:
- TOKEN
- ROOT_PASS
- KALI_PACKAGE
- VNC
- VNC_USERNAME

### Available StackScript Parameters:
- `user_name`: The limited sudo user to be created (default: "myuser")
- `disable_root`: Disable root access over SSH (default: "No")
- `kali_package`: Kali Linux package to install - Everything (~34GB), Default (~13GB), Core (~1.5GB) (default: "Default")
- `vnc`: Setup VNC remote desktop access - recommended for Everything package, adds desktop to Default/Core (default: "No")
- `vnc_username`: VNC user to be created (required if vnc="Yes"; password auto-generated)

SHELL:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export KALI_PACKAGE="Default"
export VNC="No"
export VNC_USERNAME="kaliuser"

curl -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -X POST -d '{
      "backups_enabled": true,
      "swap_size": 512,
      "image": "linode/ubuntu2404",
      "root_pass": "${ROOT_PASS}",
      "stackscript_id": 00000000000,
      "stackscript_data": {
        "user_name": "myuser",
        "disable_root": "No",
        "kali_package": "${KALI_PACKAGE}",
        "vnc": "'${VNC}'",
        "vnc_username": "${VNC_USERNAME}"
      },
      "authorized_users": [
        "myUser",
        "secondaryUser"
      ],
      "booted": true,
      "label": "linode123",
      "type": "g6-standard-2",
      "region": "us-east",
      "group": "Linode-Group"
    }' \
https://api.linode.com/v4/linode/instances
```

CLI:
```
export TOKEN="YOUR API TOKEN"
export ROOT_PASS="aComplexP@ssword"
export KALI_PACKAGE="Default"
export VNC="No"
export VNC_USERNAME="kaliuser"

linode-cli linodes create \
  --label linode123 \
  --root_pass ${ROOT_PASS} \
  --booted true \
  --stackscript_id 00000000000 \
  --stackscript_data "{"user_name": "myuser", "disable_root": "No", "kali_package": "${KALI_PACKAGE}", "vnc": "${VNC}", "vnc_username": "${VNC_USERNAME}"}" \
  --region us-east \
  --type g6-standard-2 \
  --authorized_keys "ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer"
  --authorized_users "myUser"
  --authorized_users "secondaryUser"
```

## Resources

- [Create Linode via API](https://www.linode.com/docs/api/linode-instances/#linode-create)
- [Stackscript reference](https://www.linode.com/docs/guides/writing-scripts-for-use-with-linode-stackscripts-a-tutorial/#user-defined-fields-udfs)
- [Kali Linux Documentation](https://www.kali.org/docs/)
- [VNC Remote Desktop Setup](https://www.linode.com/docs/marketplace-docs/guides/kali-linux/)

