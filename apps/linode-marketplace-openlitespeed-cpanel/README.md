# cPanel & WHM with LiteSpeed Enterprise Quick Deploy App

cPanel & WHM is a widely used Linux server/website administration platform for managing web
hosting, DNS, databases, email, and more through a browser-based interface. This Quick Deploy App
installs cPanel & WHM on Akamai Cloud Compute and layers **LiteSpeed Web Server Enterprise** on
top as the site-serving web server (replacing Apache), giving hosted sites LiteSpeed's
performance and built-in LSCache WordPress acceleration. LiteSpeed Enterprise ships on a
**15-day trial license** (see [Post-Deployment](#post-deployment)); cPanel itself ships unlicensed,
matching how every cPanel one-click across every marketplace works — activation is a manual
step the customer takes after deploy.

## Software Included

| Software | Version | Description |
| :---     | :----   | :---        |
| cPanel & WHM | latest (11.136+) | Server/website administration control panel |
| LiteSpeed Web Server | Enterprise, latest (6.3.5 at time of writing) | High-performance web server replacing Apache; ships on a 15-day trial license |

**Supported Distributions:**

- AlmaLinux 10

## Post-Deployment

- **Log in to WHM** at `https://<your-server-ip-or-rdns>:2087` as `root`, using the root password
  set when the Linode was created. (SSH in as root and the login banner prints a one-time
  `whmlogin` autologin URL automatically.)
- **Create your first cPanel account** from WHM → *Create a New Account*. Once created, log in to
  cPanel itself at `https://<your-server-ip-or-rdns>:2083` with that account's credentials.
- **Log in to the LiteSpeed WebAdmin console** at `https://<your-server-ip-or-rdns>:7080` with
  username `admin` and the password in `/root/.credentials` (generated fresh per deploy).
- **Activate your licenses.** cPanel ships unlicensed and LiteSpeed ships on a 15-day trial
  (extendable once to 30 days via LiteSpeed support) — both are fully functional during
  evaluation; a production deployment needs a cPanel license and either a purchased LiteSpeed
  Enterprise license or a renewed trial.
- Webmail is available at `https://<your-server-ip-or-rdns>:2096` per cPanel account.

## Use our API

Customers can deploy this app through the Akamai Cloud Marketplace or directly using the API.
Before using the commands below, create an [API token](https://www.linode.com/docs/products/tools/linode-api/get-started/#create-an-api-token)
or configure [linode-cli](https://www.linode.com/products/cli/), and substitute your own values
for the defaults. This app has no UDFs, so `stackscript_data` is empty.

SHELL:
```
curl -H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-X POST -d '{
    "image": "linode/almalinux10",
    "region": "us-ord",
    "type": "g6-dedicated-4",
    "label": "openlitespeed-cpanel-occ-us-ord",
    "tags": [],
    "root_pass": "A_Secure_Password",
    "authorized_users": [
        "user1",
        "user2"
    ],
    "booted": true,
    "backups_enabled": false,
    "private_ip": false,
    "stackscript_id": 00000,
    "stackscript_data": {}
}' https://api.linode.com/v4/linode/instances
```

CLI:
```
linode-cli linodes create \
  --image 'linode/almalinux10' \
  --region us-ord \
  --type g6-dedicated-4 \
  --label openlitespeed-cpanel-occ-us-ord \
  --root_pass A_Secure_Password \
  --authorized_users user1 \
  --authorized_users user2 \
  --booted true \
  --backups_enabled false \
  --private_ip false \
  --stackscript_id 000000 \
  --stackscript_data '{}'
```

## Resources

- [cPanel & WHM Documentation](https://docs.cpanel.net/)
- [LiteSpeed WHM Plugin Documentation](https://docs.litespeedtech.com/lsws/cp/cpanel/whm-litespeed-plugin/whm-install/)
- [LiteSpeed Trial License](https://docs.litespeedtech.com/lsws/trial/)
- [Akamai Quick Deploy App Guide](https://www.akamai.com/cloud/marketplace-docs/guides/litespeed-cpanel)
