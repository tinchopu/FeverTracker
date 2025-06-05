# Fever Tracker Linux Service Deployment Guide

This guide explains how to deploy your Fever Tracker application as a systemd service on Linux.

## Quick Deployment

The easiest way to deploy is using the automated deployment script:

```bash
# Make the script executable (if not already)
chmod +x deploy_as_service.sh

# Run the deployment script
./deploy_as_service.sh
```

This script will automatically:
1. Create a dedicated user `fevertracker_user`
2. Set up the application in `/opt/fevertracker`
3. Install dependencies using `uv`
4. Create and enable the systemd service
5. Start the service

## Manual Deployment Steps

If you prefer to deploy manually, follow these steps:

### 1. Create a dedicated user
```bash
sudo useradd -r -s /bin/false fevertracker_user
```

### 2. Create application directory and copy files
```bash
sudo mkdir -p /opt/fevertracker
sudo cp -r . /opt/fevertracker/
sudo chown -R fevertracker_user:fevertracker_user /opt/fevertracker
sudo chmod -R 755 /opt/fevertracker
```

### 3. Install dependencies
```bash
cd /opt/fevertracker
sudo -u fevertracker_user uv sync
```

### 4. Install the systemd service
```bash
sudo cp fever_tracker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fever_tracker.service
sudo systemctl start fever_tracker.service
```

## Service Management

Once deployed, you can manage the service using these commands:

### Check service status
```bash
sudo systemctl status fever_tracker.service
```

### View service logs
```bash
# View recent logs
sudo journalctl -u fever_tracker.service

# Follow logs in real-time
sudo journalctl -u fever_tracker.service -f
```

### Start/Stop/Restart service
```bash
sudo systemctl start fever_tracker.service
sudo systemctl stop fever_tracker.service
sudo systemctl restart fever_tracker.service
```

### Enable/Disable auto-start on boot
```bash
sudo systemctl enable fever_tracker.service   # Enable auto-start
sudo systemctl disable fever_tracker.service  # Disable auto-start
```

## Accessing the Application

Once the service is running, you can access your Fever Tracker application at:

```
http://your_server_ip:8501
```

Replace `your_server_ip` with the actual IP address of your Linux server.

## Configuration

The service configuration is defined in `fever_tracker.service`:

- **User**: `fevertracker_user` (dedicated non-privileged user)
- **Working Directory**: `/opt/fevertracker`
- **Port**: `8501`
- **Auto-restart**: Enabled (restarts automatically if it crashes)
- **Logs**: Available via `journalctl`

## Troubleshooting

### Service won't start
1. Check the service status:
   ```bash
   sudo systemctl status fever_tracker.service
   ```

2. Check the logs for error messages:
   ```bash
   sudo journalctl -u fever_tracker.service -n 50
   ```

### Common issues
- **Permission errors**: Ensure `/opt/fevertracker` is owned by `fevertracker_user`
- **Missing dependencies**: Run `sudo -u fevertracker_user uv sync` in `/opt/fevertracker`
- **Port conflicts**: Check if port 8501 is already in use with `sudo netstat -tlnp | grep 8501`

### Updating the application
To update the application:

1. Stop the service:
   ```bash
   sudo systemctl stop fever_tracker.service
   ```

2. Update the files in `/opt/fevertracker`

3. Install any new dependencies:
   ```bash
   cd /opt/fevertracker
   sudo -u fevertracker_user uv sync
   ```

4. Start the service:
   ```bash
   sudo systemctl start fever_tracker.service
   ```

## Security Considerations

- The service runs under a dedicated, non-privileged user (`fevertracker_user`)
- The application is accessible on port 8501 - consider using a firewall to restrict access
- For production use, consider setting up a reverse proxy (Nginx/Apache) with SSL/TLS

## Files Created

The deployment creates these files:
- `/etc/systemd/system/fever_tracker.service` - systemd service definition
- `/opt/fevertracker/` - application directory
- System user: `fevertracker_user`
