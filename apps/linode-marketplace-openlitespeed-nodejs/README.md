# OpenLiteSpeed Node.js

# [IN PROGRESS]
Deploys [OpenLiteSpeed](https://openlitespeed.org/) as a web server and application server for
Node.js on Ubuntu 24.04, with a sample Node.js application served over HTTPS.

Node.js runs under OpenLiteSpeed via LSAPI (`appType node`) rather than as a standalone service —
OpenLiteSpeed spawns the application per request and is itself the TLS-terminating web tier, so no
separate reverse proxy is involved.

## Software included

| Software | Version | Description |
|----------|---------|-------------|
| OpenLiteSpeed | Latest | High-performance, open source web server |
| Node.js | 26.x | JavaScript runtime, from the NodeSource repository |
| Certbot | Latest | Let's Encrypt client for SSL/TLS certificates |
| UFW | Latest | Firewall utility (ports 22, 80, 443, 7080) |
| Fail2ban | Latest | Intrusion prevention |

## Deployment
