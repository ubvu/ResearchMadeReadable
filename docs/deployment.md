
# Deployment Guide for Research made Readable

This guide provides instructions for deploying the Research made Readable application on an external Virtual Machine (VM).

## Prerequisites

- Ubuntu 20.04 LTS or later
- Python 3.8 or higher
- PostgreSQL 12 or higher
- 4GB RAM minimum (8GB recommended)
- 20GB disk space minimum

## VM Setup

### 1. Initial Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor postgresql postgresql-contrib

# Create application user
sudo useradd -m -s /bin/bash research-made-readable
sudo usermod -aG sudo research-made-readable
```

### 2. Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE research_made_readable;
CREATE USER research_made_readable WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE research_made_readable TO research_made_readable;
\q

# Configure PostgreSQL
sudo nano /etc/postgresql/12/main/postgresql.conf
# Uncomment and set: listen_addresses = 'localhost'

sudo nano /etc/postgresql/12/main/pg_hba.conf
# Add line: local   research_made_readable    research_made_readable                    md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### 3. Application Deployment

```bash
# Switch to application user
sudo -u research-made-readable -i

# Clone the application
git clone <repository-url> /home/research-made-readable/research_summary_app
cd /home/research-made-readable/research_summary_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
DATABASE_URL=postgresql://research_made_readable:your_secure_password@localhost/research_made_readable
ABACUSAI_API_KEY=your_api_key_here
EOF

# Set permissions
chmod 600 .env

# Initialize database
python setup.py
```

### 4. Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/research-made-readable

# Add configuration:
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/research-made-readable /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Supervisor Configuration

```bash
# Create supervisor configuration
sudo nano /etc/supervisor/conf.d/research-made-readable.conf

# Add configuration:
[program:research-made-readable]
command=/home/research-made-readable/research_summary_app/venv/bin/streamlit run app.py --server.port=8501 --server.address=localhost
directory=/home/research-made-readable/research_summary_app
user=research-made-readable
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/research-made-readable.log
environment=PATH="/home/research-made-readable/research_summary_app/venv/bin"

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start research-made-readable
```

### 6. SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your_domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Maintenance

### 1. Application Monitoring

```bash
# Check application status
sudo supervisorctl status research-made-readable

# View logs
sudo tail -f /var/log/research-made-readable.log

# Restart application
sudo supervisorctl restart research-made-readable
```

### 2. Database Maintenance

```bash
# Backup database
sudo -u postgres pg_dump research_made_readable > backup_$(date +%Y%m%d).sql

# Restore database
sudo -u postgres psql research_made_readable < backup_20240101.sql

# Database maintenance
sudo -u postgres psql research_made_readable -c "VACUUM ANALYZE;"
```

### 3. System Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd /home/research-made-readable/research_summary_app
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart services
sudo supervisorctl restart research-made-readable
```

## Security Considerations

### 1. Firewall Configuration

```bash
# Install UFW
sudo apt install ufw

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. Application Security

```bash
# Set proper file permissions
sudo chown -R research-made-readable:research-made-readable /home/research-made-readable/research_summary_app
sudo chmod -R 755 /home/research-made-readable/research_summary_app
sudo chmod 600 /home/research-made-readable/research_summary_app/.env

# Configure secure headers in Nginx
sudo nano /etc/nginx/sites-available/research-made-readable
# Add to server block:
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```

### 3. Database Security

```bash
# Secure PostgreSQL
sudo nano /etc/postgresql/12/main/postgresql.conf
# Set: ssl = on
# Set: password_encryption = scram-sha-256

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## Backup and Recovery

### 1. Automated Backups

```bash
# Create backup script
sudo nano /home/research-made-readable/backup.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/research-made-readable/backups"
mkdir -p $BACKUP_DIR

# Database backup
sudo -u postgres pg_dump research_made_readable > $BACKUP_DIR/db_backup_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /home/research-made-readable/research_summary_app

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

# Make executable
sudo chmod +x /home/research-made-readable/backup.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /home/research-made-readable/backup.sh
```

### 2. Recovery Procedures

```bash
# Restore database
sudo -u postgres psql research_made_readable < /home/research-made-readable/backups/db_backup_YYYYMMDD_HHMMSS.sql

# Restore application
tar -xzf /home/research-made-readable/backups/app_backup_YYYYMMDD_HHMMSS.tar.gz -C /

# Restart services
sudo supervisorctl restart research-made-readable
```

## Performance Optimization

### 1. Database Optimization

```bash
# Configure PostgreSQL for performance
sudo nano /etc/postgresql/12/main/postgresql.conf

# Recommended settings:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
max_connections = 100
```

### 2. Application Optimization

```bash
# Configure Streamlit for production
nano /home/research-made-readable/research_summary_app/.streamlit/config.toml

[server]
maxUploadSize = 200
maxMessageSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#2563EB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#1F2937"
```

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Check supervisor logs: `sudo tail -f /var/log/researchlens.log`
   - Verify environment variables in `.env`
   - Check database connectivity

2. **Database connection issues**
   - Verify PostgreSQL is running: `sudo systemctl status postgresql`
   - Check database credentials
   - Review PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-12-main.log`

3. **Nginx errors**
   - Check Nginx configuration: `sudo nginx -t`
   - Review Nginx logs: `sudo tail -f /var/log/nginx/error.log`

4. **SSL certificate issues**
   - Check certificate status: `sudo certbot certificates`
   - Renew certificate: `sudo certbot renew`

### Performance Issues

1. **Slow database queries**
   - Check database indexes
   - Run VACUUM ANALYZE
   - Monitor query performance

2. **High memory usage**
   - Monitor with `htop` or `top`
   - Adjust Streamlit configuration
   - Consider upgrading server resources

## Maintenance Schedule

### Daily
- Monitor application logs
- Check system resources
- Verify backup completion

### Weekly
- Review security logs
- Update system packages
- Check disk space usage

### Monthly
- Analyze application performance
- Review database performance
- Update application dependencies
- Security audit

---

This deployment guide provides a comprehensive setup for production deployment of Research made Readable on an external VM. Adjust configurations based on your specific requirements and security policies.
