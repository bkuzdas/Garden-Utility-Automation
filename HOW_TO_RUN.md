# 🚀 HOW TO RUN - Garden Automation System
## Complete Step-by-Step Running Instructions
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 📍 **You Are Here: System Startup Guide**

This guide shows you **exactly how to run** the Garden Automation System from start to finish.

**Choose your path:**
- **[Quick Start](#-quick-start-30-minutes)** - Get running in 30 minutes
- **[Software Only](#-software-only-no-hardware)** - Test without ESP32 hardware
- **[Detailed Setup](#-detailed-setup-full-deployment)** - Complete production deployment
- **[Troubleshooting](#-troubleshooting)** - Fix common issues

---

## ⚡ **Quick Start (30 Minutes)**

### **Prerequisites**

Before you begin, you need:
- ✅ Linux server (Raspberry Pi or x86) with Docker installed
- ✅ This repository downloaded/cloned
- ✅ (Optional) ESP32 hardware and sensors assembled

**Don't have Docker?** See [Docker Installation](#docker-installation) below.

---

### **Step 1: Configure Settings (5 minutes)**

```bash
# 1. Clone the repository (if you haven't already)
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git

# 2. Navigate to project directory
cd Garden-Utility-Automation

# 2. Copy environment template
cp env.example .env

# 3. Edit configuration
nano .env
```

**REQUIRED Changes in `.env`:**
```bash
# Your WiFi network (for ESP32 devices)
WIFI_SSID=YourActualWiFiName        # Change this!
WIFI_PASSWORD=YourActualPassword     # Change this!

# Your location (get from Google Maps)
LATITUDE=43.0731                     # Your latitude
LONGITUDE=-89.4012                   # Your longitude

# Security passwords (IMPORTANT: Change these!)
MQTT_PASSWORD=YourSecurePassword123  # Change this!
ESPHOME_OTA_PASSWORD=OTAPassword456  # Change this!
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

```bash
# 4. Copy Home Assistant secrets
cp home-assistant/secrets.yaml.example home-assistant/secrets.yaml

# 5. Edit secrets
nano home-assistant/secrets.yaml
```

Fill in the values, then save (Ctrl+X, Y, Enter).

---

### **Step 2: Start Docker Containers (5 minutes)**

```bash
# Start all services in background
docker-compose up -d

# Check status (should show "Up")
docker-compose ps
```

**Expected Output:**
```
NAME                       STATUS              PORTS
garden_homeassistant       Up 30 seconds       (host network)
garden_mqtt_broker         Up 30 seconds       1883/tcp, 9001/tcp
garden_esphome_dashboard   Up 30 seconds       6052/tcp
```

**View logs (optional):**
```bash
# Watch all services
docker-compose logs -f

# Or specific service
docker-compose logs -f homeassistant

# Press Ctrl+C to stop watching
```

---

### **Step 3: Access Home Assistant (5 minutes)**

1. **Find your server's IP address:**
   ```bash
   hostname -I    # Linux
   ipconfig       # Windows
   ```

2. **Open web browser and go to:**
   ```
   http://YOUR_SERVER_IP:8123
   ```
   - Example: `http://192.168.1.100:8123`
   - If on same computer: `http://localhost:8123`

3. **Complete the onboarding wizard:**
   - Create username and password (save these!)
   - Name: `Garden Automation` (or your choice)
   - Confirm location (should match your .env)
   - Skip integrations (we'll add later)
   - Click **"Finish"**

4. **You're in!** You should see the Home Assistant dashboard.

---

### **Step 4: Flash ESP32 Controllers (10 minutes per device)**

**⚠️ REQUIRES: ESP32 hardware and USB cable**

1. **Open ESPHome Dashboard:**
   ```
   http://YOUR_SERVER_IP:6052
   ```
   Example: `http://192.168.1.100:6052`

2. **You should see your configured devices:**
   - `esp32-garden-zone-a`
   - `esp32-garden-zone-b` (if configured)
   - `esp32-utility-control`

3. **Connect ESP32 to your computer:**
   - Use a USB cable (micro-USB or USB-C depending on board)
   - Connect ESP32 to the computer running your browser

4. **Flash the firmware:**
   - Click **"Install"** on `esp32-garden-zone-a`
   - Choose **"Plug into this computer"**
   - Select the USB port from dropdown:
     - Windows: `COM3`, `COM4`, etc.
     - Linux: `/dev/ttyUSB0`, `/dev/ttyUSB1`
     - Mac: `/dev/cu.usbserial-*`
   - Click **"Install"**
   - Wait 3-5 minutes (compilation + upload)

5. **Verify connection:**
   - Check logs for: `"WiFi connected, IP: 192.168.x.x"`
   - Check logs for: `"Connected to Home Assistant API"`
   - Note: After first USB flash, all future updates are wireless!

6. **Repeat for other ESP32s** (if you have multiple)

---

### **Step 5: Test the System (5 minutes)**

1. **In Home Assistant, navigate to:**
   ```
   Settings → Devices & Services → Devices
   ```

2. **Click on `esp32-garden-zone-a`**

3. **You should see entities:**
   - `sensor.zone_a_soil_moisture` (shows %)
   - `sensor.zone_a_flow_rate` (shows L/min)
   - `switch.zone_a_valve` (ON/OFF control)
   - `binary_sensor.zone_a_controller_status` (Online/Offline)

4. **Test the valve switch:**
   - Click on `switch.zone_a_valve`
   - Toggle it **ON**
   - **Listen for relay click** (you should hear it)
   - Toggle it **OFF**
   - **If you hear clicks, it's working!** ✅

---

### **🎉 You're Running!**

Your system is now operational! Next steps:
- **Calibrate sensors**: See `docs/CALIBRATION.md`
- **Set watering schedules**: Settings → Automations
- **Configure thresholds**: Settings → Helpers
- **Test watering**: Developer Tools → Services → `script.water_zone`

---

## 💻 **Software Only (No Hardware)**

Want to explore the system without ESP32 hardware? You can!

### **Run Containers Only**

```bash
# Start the Docker containers
cd Garden-Utility-Automation
docker-compose up -d

# Access Home Assistant
# Browser: http://localhost:8123
```

**What you can do:**
- ✅ Explore Home Assistant interface
- ✅ View all automations and logic
- ✅ Edit configurations
- ✅ Test weather integration
- ✅ Learn the system

**What you can't do:**
- ❌ Control actual valves/pumps
- ❌ Read real sensor data
- ❌ Test physical watering

### **Validate ESP32 Configs**

Check if your ESP32 configurations are valid:

```bash
# Validate Zone A config
docker exec -it garden_esphome_dashboard \
  esphome config /config/esp32_garden_zone_a.yaml

# Should show: "Configuration is valid!"
```

---

## 📖 **Detailed Setup (Full Deployment)**

For a complete production deployment with hardware:

**See:** `docs/DEPLOYMENT.md`

This includes:
- Phase 1: Server Setup (Docker installation)
- Phase 2: Start Docker Containers
- Phase 3: Hardware Assembly (wiring diagrams)
- Phase 4: ESP32 Programming
- Phase 5: Calibration
- Phase 6: Automation Configuration
- Phase 7: Monitoring Setup
- Phase 8: System Verification
- Phase 9: Production Deployment

---

## 🔧 **Common Commands**

### **Start/Stop System**

```bash
# Start all containers
docker-compose up -d

# Stop all containers (keeps data)
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Restart specific service
docker-compose restart homeassistant

# Restart everything
docker-compose restart
```

### **View Logs**

```bash
# All services (live)
docker-compose logs -f

# Specific service (live)
docker-compose logs -f homeassistant
docker-compose logs -f mqtt
docker-compose logs -f esphome

# Last 50 lines only
docker-compose logs --tail=50 homeassistant

# Save logs to file
docker-compose logs > system_logs.txt
```

### **Update System**

```bash
# Pull latest Docker images
docker-compose pull

# Recreate containers with new images
docker-compose up -d

# Check versions
docker-compose images
```

### **Backup System**

```bash
# Manual backup
./scripts/backup.sh

# Or use Docker commands
tar -czf backup.tar.gz home-assistant esphome mqtt
```

---

## 🌐 **Access URLs**

Once running, access these web interfaces:

| Service | URL | What It Does |
|---------|-----|--------------|
| **Home Assistant** | `http://YOUR_IP:8123` | Main dashboard, automations, controls |
| **ESPHome Dashboard** | `http://YOUR_IP:6052` | ESP32 firmware management, OTA updates |
| **MQTT Broker** | `mqtt://YOUR_IP:1883` | No web UI (backend messaging) |

**Replace `YOUR_IP` with your server's IP address**

---

## 🐛 **Troubleshooting**

### **"Command not found: docker-compose"**

**Problem:** Docker not installed or not in PATH.

**Solution:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in (IMPORTANT!)
```

---

### **"Cannot connect to Home Assistant"**

**Problem:** Wrong IP address or service not started.

**Solution:**
```bash
# Check if containers are running
docker-compose ps

# If not running, start them
docker-compose up -d

# Find your server's IP
hostname -I

# Try: http://THAT_IP:8123
```

---

### **"Home Assistant shows error on startup"**

**Problem:** Usually missing secrets.yaml or configuration error.

**Solution:**
```bash
# Check logs for specific error
docker-compose logs homeassistant | grep -i error

# Common fix: secrets.yaml missing
cp home-assistant/secrets.yaml.example home-assistant/secrets.yaml
nano home-assistant/secrets.yaml

# Restart after fixing
docker-compose restart homeassistant
```

---

### **"ESP32 won't connect to WiFi"**

**Problem:** Wrong WiFi credentials or weak signal.

**Solution:**
```bash
# 1. Verify credentials in .env
nano .env
# Check WIFI_SSID and WIFI_PASSWORD

# 2. Check WiFi signal strength at ESP32 location
# (Use phone WiFi analyzer app)

# 3. Check ESP32 logs in ESPHome Dashboard
# Look for: "WiFi connection failed"

# 4. If needed, re-flash with correct credentials
```

---

### **"Sensors show 'Unknown' or 'Unavailable'"**

**Problem:** Wiring issue or ESP32 offline.

**Solution:**
```bash
# 1. Check ESP32 is online
# Home Assistant → Settings → Devices
# Should show "Online"

# 2. Check wiring connections
# Verify GPIO pin assignments match YAML config

# 3. Restart ESP32
# Home Assistant → switch.restart_esp32 → Turn On

# 4. Check sensor logs
# ESPHome Dashboard → Logs (for that device)
```

---

### **"Port already in use" error**

**Problem:** Another service using ports 8123, 1883, or 6052.

**Solution:**
```bash
# Check what's using the port
sudo lsof -i :8123

# Stop conflicting service
sudo systemctl stop <service_name>

# Or change port in docker-compose.yml
nano docker-compose.yml
# Change "8123:8123" to "8124:8123"
```

---

### **"Permission denied" errors**

**Problem:** User not in docker group.

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# MUST log out and back in!
# Or run: newgrp docker

# Test
docker ps
# Should work without sudo
```

---

## 🔐 **Security Checklist**

Before exposing to network:

- [ ] Changed default MQTT password in `.env`
- [ ] Changed OTA password in `.env`
- [ ] Created strong Home Assistant password
- [ ] Enabled Home Assistant 2FA (Settings → Profile)
- [ ] Configured firewall (if exposing to internet)
- [ ] Secrets.yaml not committed to Git (.gitignore blocks it)
- [ ] Regular backups scheduled

---

## 📊 **System Health Check**

Run this after starting to verify everything:

```bash
# Check all containers running
docker-compose ps

# Check Home Assistant
curl -s http://localhost:8123 | grep -q "Home Assistant" && echo "✓ HA Running"

# Check MQTT
docker-compose logs mqtt | grep -q "mosquitto version" && echo "✓ MQTT Running"

# Check ESPHome
curl -s http://localhost:6052 | grep -q "ESPHome" && echo "✓ ESPHome Running"
```

Or use the monitoring script:

```bash
# Install dependencies first
pip3 install requests paho-mqtt

# Run health check (requires HA token)
python3 scripts/monitor.py --ha-token YOUR_TOKEN
```

---

## 📚 **Next Steps After Running**

### **Immediate (Today)**
1. ✅ Verify all containers running
2. ✅ Access Home Assistant dashboard
3. ✅ Flash ESP32s (if you have hardware)
4. ✅ Test valve switches
5. ✅ Check sensor readings

### **Soon (This Week)**
1. 📏 Calibrate sensors → `docs/CALIBRATION.md`
2. ⚙️ Configure thresholds (Settings → Helpers)
3. ⏰ Set watering schedules
4. 🧪 Test first watering cycle
5. 🔔 Setup notifications

### **Later (This Month)**
1. 📊 Monitor water usage
2. 🔧 Fine-tune watering durations
3. 🌦️ Verify weather integration working
4. 💾 Setup automated backups
5. 📱 Configure mobile app

---

## 🎯 **Quick Reference Card**

**Print this out for easy reference:**

```
╔══════════════════════════════════════════════════════╗
║     GARDEN AUTOMATION - QUICK REFERENCE              ║
╠══════════════════════════════════════════════════════╣
║ Start System:    docker-compose up -d                ║
║ Stop System:     docker-compose stop                 ║
║ View Logs:       docker-compose logs -f              ║
║                                                       ║
║ Home Assistant:  http://YOUR_IP:8123                 ║
║ ESPHome:         http://YOUR_IP:6052                 ║
║                                                       ║
║ Config Location: ./home-assistant/                   ║
║ ESP32 Configs:   ./esphome/                          ║
║                                                       ║
║ Backup:          ./scripts/backup.sh                 ║
║ Monitor:         python3 scripts/monitor.py          ║
╚══════════════════════════════════════════════════════╝
```

---

## 📞 **Getting Help**

### **Documentation**
- This guide: `HOW_TO_RUN.md` ← You are here
- Quick start: `QUICKSTART.md`
- Full deployment: `docs/DEPLOYMENT.md`
- Calibration: `docs/CALIBRATION.md`
- Wisconsin climate: `docs/WISCONSIN_CLIMATE.md`

### **Logs**
```bash
docker-compose logs -f [service_name]
```

### **Community**
- Home Assistant Forums: https://community.home-assistant.io/
- ESPHome Discord: https://discord.gg/KhAMKrd

### **Project**
- GitHub Repository: https://github.com/bkuzdas/Garden-Utility-Automation
- GitHub Issues: https://github.com/bkuzdas/Garden-Utility-Automation/issues

---

## ✅ **Success Checklist**

After following this guide, you should have:

- [x] All Docker containers running
- [x] Home Assistant accessible via browser
- [x] ESPHome Dashboard accessible
- [x] ESP32(s) flashed and connected (if hardware available)
- [x] Sensors showing values in Home Assistant
- [x] Switches controlling relays
- [x] Weather integration working
- [x] Automations enabled

**If all checked, you're ready to start automating your garden! 🌱💧**

---

## 🎉 **Congratulations!**

Your Garden Automation System is now running! 

**What's happening now:**
- 🐳 Docker containers are managing the software
- 🏠 Home Assistant is monitoring conditions
- 📡 ESP32s are reading sensors and controlling valves
- 🌦️ Weather data is being integrated
- ⚙️ Automations are ready to run

**Enjoy your automated garden!**

---

**Garden & Utility Automation System**  
**By Brian Kuzdas - 03/02/2024**  
**Copyright (c) 2024 Brian Kuzdas**

