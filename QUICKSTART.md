# 🚀 Quick Start Guide
## Get Your Garden Automation Running in 30 Minutes
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## ⚡ For the Impatient

### Step 1: Clone & Configure (5 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/Garden-Utility-Automation.git
cd Garden-Utility-Automation

# Copy and edit environment file
cp env.example .env
nano .env
# Change: WIFI_SSID, WIFI_PASSWORD, MQTT_PASSWORD, LATITUDE, LONGITUDE
# Save: Ctrl+X, Y, Enter

# Copy Home Assistant secrets
cp home-assistant/secrets.yaml.example home-assistant/secrets.yaml
nano home-assistant/secrets.yaml
# Fill in your values
# Save and exit
```

### Step 2: Start Docker Containers (10 minutes)

```bash
# Start everything
docker-compose up -d

# Wait 2 minutes, then check status
docker-compose ps

# Access Home Assistant
# Open browser: http://YOUR_IP:8123
# Complete setup wizard
```

### Step 3: Flash ESP32 (10 minutes)

```bash
# Open ESPHome Dashboard
# Browser: http://YOUR_IP:6052

# Connect ESP32 via USB
# Click "Install" on your device
# Choose "Plug into this computer"
# Select USB port
# Wait for upload (~5 minutes)
```

### Step 4: Test (5 minutes)

```bash
# In Home Assistant:
# 1. Go to Settings → Devices
# 2. Find your ESP32
# 3. Toggle valve switch
# 4. Verify it clicks on/off
# 5. Check soil moisture sensor shows a value

# Done! 🎉
```

---

## 📚 Full Documentation

- **Detailed Setup**: See `docs/DEPLOYMENT.md`
- **Calibration**: See `docs/CALIBRATION.md`
- **Wisconsin Climate**: See `docs/WISCONSIN_CLIMATE.md`
- **Main README**: See `README.md`

---

## 🆘 Something Broken?

### Home Assistant Won't Start
```bash
# Check logs
docker-compose logs homeassistant

# Common issue: secrets.yaml missing
# Solution: Copy from secrets.yaml.example
```

### ESP32 Won't Connect
```bash
# Check WiFi credentials in .env file
# Verify WiFi signal strength at installation location
# Check ESPHome logs for errors
```

### Sensors Show "Unknown"
```bash
# Verify wiring connections
# Check GPIO pin assignments in YAML files
# Restart ESP32: Home Assistant → switch.restart_esp32
```

---

## ✅ Next Steps After Quick Start

1. **Calibrate Sensors**: Follow `docs/CALIBRATION.md`
2. **Set Watering Schedule**: Home Assistant → Automations
3. **Configure Thresholds**: Home Assistant → Settings → Helpers
4. **Test Automations**: Run morning watering manually
5. **Enable Monitoring**: Setup `scripts/monitor.py`
6. **Schedule Backups**: Setup `scripts/backup.sh`

---

## 📞 Need Help?

- **Documentation**: Check `/docs` folder
- **Logs**: `docker-compose logs -f`
- **Community**: Home Assistant forums
- **Issues**: GitHub issue tracker

---

**Happy Gardening!** 🌱💧

