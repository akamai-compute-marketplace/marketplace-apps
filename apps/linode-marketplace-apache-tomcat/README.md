# Linode Apache Tomcat One-Click App

Deploy Apache Tomcat, the open source Jakarta EE servlet container, on Ubuntu 24.04. Tomcat runs as an unprivileged `tomcat` systemd service and listens only on `127.0.0.1:8081`. Apache HTTP Server is the public edge: it terminates Let's Encrypt TLS on port 443, redirects HTTP to HTTPS, and reverse-proxies requests to Tomcat.

The official Tomcat sample application is deployed as the root context (`https://<your-domain>/`) so you can confirm the stack works end to end. Replace it with your own application as described below.

## Software Included

| Software      | Version       | Description                                   |
| :---          | :----         | :---                                          |
| Apache Tomcat | Latest 11.0.x | Jakarta EE 11 servlet container               |
| OpenJDK       | 17            | Java runtime                                  |
| Apache HTTP   | Latest        | TLS termination and reverse proxy             |
| Certbot       | Latest        | Let's Encrypt certificate issuance and renewal |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

| Item               | Location                                    |
| :---               | :---                                        |
| Tomcat home        | `/opt/tomcat`                               |
| Web applications   | `/opt/tomcat/webapps/`                      |
| Tomcat logs        | `/opt/tomcat/logs/` and `journalctl -u tomcat` |
| Apache vhosts      | `/etc/apache2/sites-available/tomcat.conf`, `tomcat-le-ssl.conf` |
| Credentials        | `/home/$USERNAME/.credentials`              |

Hardening applied on top of the stock Tomcat distribution:

- The default HTTP connector on port 8080 is replaced by a loopback-only connector on `127.0.0.1:8081`.
- The shutdown port is disabled (`port="-1"`).
- The bundled `ROOT`, `docs`, `examples`, `manager`, and `host-manager` applications are removed. These are protected by a localhost-only valve, which is bypassed when requests arrive through the local Apache proxy.

See the [Tomcat Security Considerations](https://tomcat.apache.org/tomcat-11.0-doc/security-howto.html) guide.

## Deploying Your Application

Tomcat auto-deploys WAR files placed in `/opt/tomcat/webapps/`. To replace the sample application with your own, copy your WAR to the server and install it as `ROOT.war`:

```
scp myapp.war $USERNAME@<your-domain>:/tmp/
ssh $USERNAME@<your-domain>
sudo systemctl stop tomcat
sudo rm -rf /opt/tomcat/webapps/ROOT /opt/tomcat/webapps/ROOT.war
sudo install -o tomcat -g tomcat -m 0640 /tmp/myapp.war /opt/tomcat/webapps/ROOT.war
sudo systemctl start tomcat
```

To serve an application under a path instead (for example `https://<your-domain>/myapp/`), install it as `/opt/tomcat/webapps/myapp.war`.

Tomcat 11 implements Jakarta EE 11 (`jakarta.*` packages). Applications built against `javax.*` APIs must be migrated first, for example with the [Apache Tomcat migration tool for Jakarta EE](https://tomcat.apache.org/download-migration.cgi).

## Linode Helpers Included

| Name              | Action |
| :---              | :---   |
| Hostname          | Sets the system hostname to the provided domain or the Linode's default rDNS. |
| Update Packages   | Performs apt update and upgrade actions as root. |
| UFW               | Enables UFW and allows ports 22, 80, and 443. |
| Fail2Ban          | Installs, activates and enables the Fail2Ban service. |
| Create DNS Record | Creates DNS records for the domain and subdomain using the Linode API. |
| Secure SSH        | Disables root login and password authentication when requested. |
| SSH Key           | Deploys SSH keys for the sudo user. |
| Certbot SSL       | Issues a Let's Encrypt certificate with the Apache plugin and configures HTTP to HTTPS redirects. |

## Resources

- [Apache Tomcat 11 Documentation](https://tomcat.apache.org/tomcat-11.0-doc/)
- [Tomcat Proxy Configuration](https://tomcat.apache.org/tomcat-11.0-doc/proxy-howto.html)
- [Tomcat Security Considerations](https://tomcat.apache.org/tomcat-11.0-doc/security-howto.html)
- [Apache HTTP Server mod_proxy](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html)
