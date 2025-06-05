# Fever Tracker Service Troubleshooting Guide

## Common Issues and Solutions

### 1. Permission Denied Error when Starting Service

**Symptoms:**
- Service fails to start with "Permission denied (os error 13)"
- Error message: "error: Failed to spawn: `streamlit`"

**Root Cause:**
The service user doesn't have access to the `uv` executable or the Python virtual environment, or there are permission issues with the user's home directory or cache.

**Quick Fix:**
Run the automated fix script:
```bash
sudo ./fix_service_permissions.sh
```

**Manual Solution:**
If the automated script doesn't work, follow these steps:

1. **Stop the service:**
   ```bash
   sudo systemctl stop fever_tracker.service
   ```

2. **Fix user directories:**
   ```bash
   sudo mkdir -p /home/fevertracker_user/.local/bin
   sudo mkdir -p /home/fevertracker_user/.cache
   sudo chown -R fevertracker_user:fevertracker_user /home/fevertracker_user
   sudo chmod -R 755 /home/fevertracker_user
   ```

3. **Reinstall uv for the service user:**
   ```bash
   sudo rm -f /home/fevertracker_user/.local/bin/uv
   sudo -u fevertracker_user bash -c 'export HOME="/home/fevertracker_user" && curl -LsSf https://astral.sh/uv/install.sh | sh'
   sudo chmod +x /home/fevertracker_user/.local/bin/uv
   ```

4. **Reinstall dependencies:**
   ```bash
   cd /opt/fevertracker
   sudo rm -rf .venv
   sudo -u fevertracker_user HOME="/home/fevertracker_user" PATH="/home/fevertracker_user/.local/bin:$PATH" /home/fevertracker_user/.local/bin/uv sync
   ```

5. **Restart the service:**
   ```bash
   sudo systemctl start fever_tracker.service
   ```

### 2. Service File Issues

**Fixed Issues:**
- Updated `StandardOutput` and `StandardError` from deprecated `syslog` to `journal`
- Added proper PATH environment variable
- Updated ExecStart to use the correct path to `uv`

### 3. Deployment Steps

If you encounter issues, follow these steps:

1. **Stop the existing service:**
   ```bash
   sudo systemctl stop fever_tracker.service
   sudo systemctl disable fever_tracker.service
   ```

2. **Clean up previous installation:**
   ```bash
   sudo rm -f /etc/systemd/system/fever_tracker.service
   sudo systemctl daemon-reload
   ```

3. **Re-run the deployment script:**
   ```bash
   sudo ./deploy_as_service.sh
   ```

### 4. Checking Service Status

**View service status:**
```bash
sudo systemctl status fever_tracker.service
```

**View detailed logs:**
```bash
sudo journalctl -u fever_tracker.service -f
```

**Check if service is running:**
```bash
sudo systemctl is-active fever_tracker.service
```

### 5. Manual Testing

To test if the application works manually:

1. **Switch to service user:**
   ```bash
   sudo -u fevertracker_user -s
   ```

2. **Navigate to app directory:**
   ```bash
   cd /opt/fevertracker
   ```

3. **Run the application manually:**
   ```bash
   /home/fevertracker_user/.local/bin/uv run streamlit run main.py --server.port 8501 --server.headless true
   ```

### 6. File Permissions

Ensure proper permissions are set:
```bash
sudo chown -R fevertracker_user:fevertracker_user /opt/fevertracker
sudo chown -R fevertracker_user:fevertracker_user /home/fevertracker_user
sudo chmod -R 755 /opt/fevertracker
sudo chmod -R 755 /home/fevertracker_user
```

### 7. Network Access

The application runs on port 8501. Ensure:
- Port 8501 is not blocked by firewall
- No other service is using port 8501

**Check port usage:**
```bash
sudo netstat -tlnp | grep 8501
```

### 8. Dependencies

If dependency installation fails:
```bash
cd /opt/fevertracker
sudo -u fevertracker_user HOME="/home/fevertracker_user" PATH="/home/fevertracker_user/.local/bin:$PATH" /home/fevertracker_user/.local/bin/uv sync --verbose
```

## Service Management Commands

- **Start service:** `sudo systemctl start fever_tracker.service`
- **Stop service:** `sudo systemctl stop fever_tracker.service`
- **Restart service:** `sudo systemctl restart fever_tracker.service`
- **Enable on boot:** `sudo systemctl enable fever_tracker.service`
- **Disable on boot:** `sudo systemctl disable fever_tracker.service`
- **View logs:** `sudo journalctl -u fever_tracker.service -f`
- **Check status:** `sudo systemctl status fever_tracker.service`
