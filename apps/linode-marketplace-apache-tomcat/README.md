# Linode Apache Tomcat One-Click App

Deploy Apache Tomcat, an open-source web server for Java-based web applications. Tomcat runs as an unprivileged `tomcat` systemd service and listens only on `127.0.0.1:8081`. An Apache HTTP Server terminates the Let's Encrypt TLS on port 443, redirects HTTP to HTTPS, and reverse-proxies requests to Tomcat.

The official Tomcat sample application is deployed as the root context (`https://<your-domain>/`) so you can confirm the stack works end-to-end. Replace it with your own application as described below.

## Software Included

| Software      | Version       | Description                                            |
| :---          | :----         | :---                                                   |
| Apache Tomcat | Latest 11.0.x | Open-source web server for Java-based web applications |
| OpenJDK       | 17            | Open-source Java runtime                               |
| Apache HTTP   | Latest        | TLS termination and reverse proxy                      |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

| Item               | Location                                    |
| :---               | :---                                        |
| Tomcat home        | `/opt/tomcat`                               |
| Web applications   | `/opt/tomcat/webapps/`                      |
| Tomcat logs        | `/opt/tomcat/logs/` and `journalctl -u tomcat` |
| Apache vhosts      | `/etc/apache2/sites-available/tomcat.conf`, `tomcat-le-ssl.conf` |

## Deploying Your Application

Tomcat redeploys WAR files placed in `/opt/tomcat/webapps/` while running. To replace the sample application at `/`:

```
scp myapp.war $USERNAME@<ip-address>:/tmp/
ssh $USERNAME@<ip-address>
sudo chown tomcat:tomcat /tmp/myapp.war
sudo chmod 0640 /tmp/myapp.war
sudo mv -f /tmp/myapp.war /opt/tomcat/webapps/ROOT.war
```

No stop, start, or manual delete is needed. Wait for redeployment, then check `https://<your-domain>/`. To add your application to a different URL path (e.g. - `/sample`), follow the above steps but use `/opt/tomcat/webapps/sample.war` instead.

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
