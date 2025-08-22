# Apache Guacamole Marketplace App

This Marketplace App deploys a production-ready Apache Guacamole remote desktop gateway on Akamai Connected Cloud (Linode). Guacamole provides secure access to remote systems via RDP, VNC, SSH, and Telnet through a web browser.

## Architecture

The deployment uses a 4-container Docker architecture following Apache Guacamole's official recommendations:

- **PostgreSQL 15**: Database backend for authentication and connection storage
- **Guacamole Daemon (guacd)**: Protocol translation service for remote connections
- **Guacamole Web App**: Web-based user interface and session management
- **NGINX**: Reverse proxy with SSL termination and security headers

## Features

- **Web-based Management**: Full user and connection management via web interface
- **Multiple Protocols**: Support for RDP, VNC, SSH, and Telnet connections
- **SSL/HTTPS**: Automatic Let's Encrypt certificates or self-signed fallback
- **Database Authentication**: PostgreSQL-based user management (production-ready)
- **Security Hardening**: UFW firewall, fail2ban, secure SSH configuration
- **Automatic Setup**: Pre-configured admin user with secure password generation

## Installation

### Prerequisites

- Akamai Connected Cloud (Linode) account
- Minimum server: 2GB RAM, 2 vCPUs (g6-standard-2 or higher recommended)
- Ubuntu 22.04 LTS

### Quick Deploy

1. **Via Linode Cloud Manager:**
   - Navigate to "Create" → "Marketplace"
   - Select "Apache Guacamole"
   - Configure your server settings
   - Deploy

2. **Via StackScript:**
   ```bash
   # Clone this repository
   git clone https://github.com/akamai-compute-marketplace/marketplace-apps.git
   cd marketplace-apps/deployment_scripts/linode-marketplace-guacamole
   
   # Run deployment script
   bash guacamole-deploy.sh
   ```

### Configuration Options

- **Email Address**: For Let's Encrypt SSL certificate (optional)
- **Admin User**: Limited sudo user creation
- **Domain Settings**: Custom domain configuration (optional)
- **SSH Security**: Option to disable root SSH access

## Access Information

### Web Interface

- **URL**: `https://your-server-ip-or-domain/`
- **Default Username**: `guacadmin`
- **Default Password**: Check `/home/username/.credentials` file

### Server Access

- **SSH**: `ssh username@your-server-ip`
- **Credentials**: Available in `/home/username/.credentials`

## Post-Installation Setup

### Creating Remote Connections

1. Log into the Guacamole web interface
2. Navigate to "Settings" → "Connections"
3. Click "New Connection"
4. Configure connection details:
   - **RDP**: Windows servers (port 3389)
   - **VNC**: Linux desktops (port 5900)
   - **SSH**: Terminal access (port 22)
   - **Telnet**: Legacy systems (port 23)

### User Management

1. Go to "Settings" → "Users"
2. Create new users and assign connection permissions
3. Configure user groups for bulk permission management

## Maintenance

### Password Management

Update the admin password:
```bash
sudo /opt/guacamole/update-guacamole-password.sh "YourNewSecurePassword"
```

### Service Management

```bash
# View service status
cd /opt/guacamole && docker compose ps

# Restart all services
cd /opt/guacamole && docker compose restart

# View logs
cd /opt/guacamole && docker compose logs

# Stop services
cd /opt/guacamole && docker compose down

# Start services
cd /opt/guacamole && docker compose up -d
```

### Database Backup

```bash
# Create database backup
cd /opt/guacamole
docker compose exec postgres pg_dump -U guacamole_user guacamole_db > guacamole_backup_$(date +%Y%m%d).sql

# Restore database backup
docker compose exec -T postgres psql -U guacamole_user guacamole_db < guacamole_backup_YYYYMMDD.sql
```

### SSL Certificate Renewal

Let's Encrypt certificates auto-renew via systemd. Manual renewal:
```bash
sudo certbot renew
cd /opt/guacamole && docker compose restart nginx
```

## File Locations

### Configuration Files
- **Docker Compose**: `/opt/guacamole/docker-compose.yml`
- **NGINX Config**: `/opt/guacamole/nginx/nginx.conf`
- **Database Init**: `/opt/guacamole/postgres-init/001-initdb.sql`

### Credentials and Logs
- **User Credentials**: `/home/username/.credentials`
- **Service Logs**: `docker compose logs` from `/opt/guacamole/`
- **System Logs**: `/var/log/stackscript.log`

### Utilities
- **Password Update**: `/opt/guacamole/update-guacamole-password.sh`

## Security

### Firewall Configuration
- Port 22 (SSH): Open
- Port 80 (HTTP): Open (redirects to HTTPS)
- Port 443 (HTTPS): Open
- PostgreSQL (5432): Internal only
- Guacd (4822): Internal only

### Security Features
- fail2ban intrusion prevention
- UFW firewall with minimal open ports
- SSL/TLS encryption for all web traffic
- Security headers (HSTS, X-Frame-Options, etc.)
- Database authentication (no static configuration files)

## Troubleshooting

### Common Issues

#### Blank Screen on Login
**Symptoms**: Browser shows blank page when accessing Guacamole
**Solution**: Check nginx logs for rate limiting errors:
```bash
cd /opt/guacamole && docker compose logs nginx | tail -20
```

#### Login Failed
**Symptoms**: "Invalid login" despite correct credentials
**Solution**: Reset admin password:
```bash
sudo /opt/guacamole/update-guacamole-password.sh "NewPassword123"
```

#### Services Not Starting
**Symptoms**: Docker containers showing error status
**Solution**: Check logs and restart:
```bash
cd /opt/guacamole
docker compose logs
docker compose down && docker compose up -d
```

### Support

- **Documentation**: [Apache Guacamole Manual](https://guacamole.apache.org/doc/gug/)
- **Docker Guide**: [Guacamole Docker Documentation](https://guacamole.apache.org/doc/gug/guacamole-docker.html)
- **Linode Support**: [Linode Community](https://www.linode.com/community/questions/)

## Technical Specifications

### System Requirements
- **Memory**: 2GB RAM minimum, 4GB recommended
- **CPU**: 2 vCPUs minimum
- **Storage**: 20GB minimum, 40GB recommended
- **OS**: Ubuntu 22.04 LTS

### Container Versions
- **Guacamole**: 1.5.5
- **PostgreSQL**: 15
- **NGINX**: 1.25

### Network Architecture
- Internal Docker bridge network: `guacamole_net`
- External access: NGINX proxy on ports 80/443
- Database and guacd: Internal access only

## Contributing

For bug reports or feature requests, please visit the [marketplace-apps repository](https://github.com/akamai-compute-marketplace/marketplace-apps).

## License

Apache Guacamole is licensed under the Apache License 2.0. This deployment configuration is provided under the same license.