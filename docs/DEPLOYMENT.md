# Deployment Guide
## Garden & Utility Automation System - Complete Setup Instructions
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 📋 Pre-Deployment Checklist

Before beginning deployment, ensure you have:

### Hardware Requirements
- [ ] Docker host server (Raspberry Pi 4+ or x86 Linux)
- [ ] 2-4 ESP32 DevKit boards
- [ ] Capacitive soil moisture sensors (1 per zone)
- [ ] Water flow sensors (YF-S201 or similar)
- [ ] Ultrasonic distance sensor (HC-SR04) for tank level
- [ ] 12V solenoid valves (1 per zone)
- [ ] 5V relay modules (sufficient channels)
- [ ] 12V water pump (if using reservoir)
- [ ] Power supplies (5V for ESP32, 12V for valves/pump)
- [ ] Weatherproof enclosures (IP65+)
- [ ] Wiring supplies (18-22 AWG)

### Software Requirements
- [ ] Linux OS installed (Debian, Ubuntu, or Raspberry Pi OS)
- [ ] Docker Engine 20.10+
- [ ] Docker Compose 2.0+
- [ ] Git
- [ ] Text editor (nano, vim, or VSCode with Remote SSH)

### Network Requirements
- [ ] Stable WiFi coverage in installation area
- [ ] Static IP or DHCP reservation for Docker host (recommended)
- [ ] Port access: 8123 (HA), 1883 (MQTT), 6052 (ESPHome)

### Knowledge Requirements
- [ ] Basic Linux command line
- [ ] Basic understanding of YAML syntax
- [ ] Basic electrical safety (working with 12V DC)

---

## 🚀 Phase 1: Server Setup

### Step 1.1: Prepare Docker Host

**Pseudo Code:**
```
UPDATE system packages
INSTALL Docker and Docker Compose
CONFIGURE Docker to start on boot
ADD user to docker group
VERIFY installation
```

**Commands:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group (replace 'pi' with your username)
sudo usermod -aG docker $USER

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify installation
docker --version
docker-compose --version

# Log out and back in for group changes to take effect
```

### Step 1.2: Clone Repository

**Pseudo Code:**
```
NAVIGATE to installation directory
CLONE repository from GitHub
CHANGE to project directory
```

**Commands:**
```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone repository
git clone https://github.com/yourusername/Garden-Utility-Automation.git
cd Garden-Utility-Automation

# Verify structure
ls -la
```

### Step 1.3: Configure Environment

**Pseudo Code:**
```
COPY environment template
EDIT environment file with your settings
SET WiFi credentials
SET MQTT passwords
SET location coordinates
```

**Commands:**
```bash
# Copy environment template
cp env.example .env

# Edit with your settings
nano .env
```

**Required Changes in `.env`:**
```bash
# Location (find your coordinates on Google Maps)
LATITUDE=43.0731
LONGITUDE=-89.4012
ELEVATION=259

# WiFi Credentials (for ESP32 devices)
WIFI_SSID=YourActualWiFiName
WIFI_PASSWORD=YourActualWiFiPassword

# MQTT Security (change these!)
MQTT_USERNAME=garden_user
MQTT_PASSWORD=SecurePassword123!

# OTA Security (for ESP32 updates)
ESPHOME_OTA_PASSWORD=OTAPassword456!
WIFI_AP_PASSWORD=FallbackPass789!
```

Save and exit (Ctrl+X, Y, Enter)

### Step 1.4: Configure Home Assistant Secrets

**Pseudo Code:**
```
COPY secrets template
FILL in passwords and API keys
SAVE secrets file
```

**Commands:**
```bash
# Copy secrets template
cp home-assistant/secrets.yaml.example home-assistant/secrets.yaml

# Edit secrets
nano home-assistant/secrets.yaml
```

Fill in your values, then save.

### Step 1.5: Configure MQTT Authentication (Optional but Recommended)

**Pseudo Code:**
```
CREATE MQTT password file
ADD users to password file
SET correct permissions
```

**Commands:**
```bash
# Create password file
# Note: This will be done after MQTT container is running
# For now, we'll use anonymous access
```

---

## 🐳 Phase 2: Start Docker Containers

### Step 2.1: First-Time Startup

**Pseudo Code:**
```
BUILD and START all containers
WAIT for initialization
CHECK container status
VIEW logs for errors
```

**Commands:**
```bash
# Start all services in detached mode
docker-compose up -d

# Check status (all should show "Up")
docker-compose ps

# View logs (Ctrl+C to exit)
docker-compose logs -f

# View logs for specific service
docker-compose logs -f homeassistant
```

**Expected Output:**
```
NAME                       STATUS              PORTS
garden_homeassistant       Up 30 seconds       (host network)
garden_mqtt_broker         Up 30 seconds       1883/tcp, 9001/tcp
garden_esphome_dashboard   Up 30 seconds       6052/tcp
```

### Step 2.2: Access Home Assistant

**Pseudo Code:**
```
OPEN web browser
NAVIGATE to Home Assistant
COMPLETE onboarding wizard
CREATE admin account
```

**Steps:**
1. Open browser: `http://YOUR_SERVER_IP:8123`
2. Complete onboarding:
   - Create username and password
   - Set name: "Garden Automation"
   - Confirm location (from .env)
   - Skip integrations for now
3. Click "Finish"

### Step 2.3: Generate Home Assistant Long-Lived Token

**Pseudo Code:**
```
LOGIN to Home Assistant
GO TO profile
CREATE long-lived access token
SAVE token securely (needed for monitoring script)
```

**Steps:**
1. Click your user profile (bottom left)
2. Scroll to "Long-Lived Access Tokens"
3. Click "Create Token"
4. Name: "Garden Monitoring Script"
5. **Copy and save the token** (you won't see it again!)

---

## 🔌 Phase 3: Hardware Assembly

### Step 3.1: ESP32 Wiring - Zone Controller

**Pseudo Code for Zone A Controller:**
```
CONNECT soil moisture sensor to GPIO34 (analog)
CONNECT flow sensor to GPIO25 (pulse input)
CONNECT valve relay to GPIO26 (digital output)
CONNECT 5V and GND
TEST connections with multimeter
```

**Wiring Diagram (Zone A):**
```
ESP32 DevKit          Component
=============         =========
GPIO34 (Input)   -->  Soil Moisture Sensor (Signal)
3.3V             -->  Soil Moisture Sensor (VCC)
GND              -->  Soil Moisture Sensor (GND)

GPIO25 (Input)   -->  Flow Sensor (Signal)
5V               -->  Flow Sensor (VCC)
GND              -->  Flow Sensor (GND)

GPIO26 (Output)  -->  Relay Module (IN1)
5V               -->  Relay Module (VCC)
GND              -->  Relay Module (GND)

Relay NO         -->  Solenoid Valve (+)
Relay COM        -->  12V Power Supply (+)
12V Power (-)    -->  Solenoid Valve (-)
```

**Safety Checks:**
- [ ] No short circuits (use multimeter continuity test)
- [ ] Correct voltage levels (5V to 5V, 3.3V to 3.3V)
- [ ] Polarity correct on solenoid valves
- [ ] Relay ratings exceed valve current draw
- [ ] All connections insulated

### Step 3.2: ESP32 Wiring - Utility Controller

**Pseudo Code:**
```
CONNECT ultrasonic sensor (trigger GPIO23, echo GPIO22)
CONNECT main flow sensor to GPIO32
CONNECT pump relay to GPIO33
CONNECT main valve relay to GPIO14
VERIFY power supply adequate (relays can draw significant current)
```

**Wiring Diagram (Utility):**
```
ESP32 DevKit          Component
=============         =========
GPIO23 (Output)  -->  Ultrasonic Trigger
GPIO22 (Input)   -->  Ultrasonic Echo
5V               -->  Ultrasonic VCC
GND              -->  Ultrasonic GND

GPIO32 (Input)   -->  Main Flow Sensor (Signal)
GPIO33 (Output)  -->  Pump Relay (IN1)
GPIO14 (Output)  -->  Main Valve Relay (IN2)

Pump Relay NO    -->  Water Pump (+)
Pump Relay COM   -->  12V Power (+)
```

### Step 3.3: Physical Installation

**Soil Moisture Sensors:**
- Insert vertically into soil (full depth)
- Position 4-6 inches from plant stem
- Ensure good soil contact
- Protect electronics from water

**Flow Sensors:**
- Install inline with water pipes
- Arrow on sensor indicates flow direction
- Use hose clamps or threaded adapters
- Mount horizontally if possible

**Valves:**
- Install normally-closed (NC) solenoid valves
- Mark zones clearly
- Ensure adequate water pressure (20-80 PSI)
- Test manual operation first

**ESP32 Controllers:**
- Place in weatherproof enclosure
- Ensure WiFi signal strength adequate (-70 dBm or better)
- Leave access for USB (initial programming)
- Provide ventilation (ESP32 generates heat)

---

## 📡 Phase 4: ESP32 Programming

### Step 4.1: Access ESPHome Dashboard

**Pseudo Code:**
```
OPEN web browser
NAVIGATE to ESPHome Dashboard
VERIFY all YAML configs are visible
```

**Steps:**
1. Open browser: `http://YOUR_SERVER_IP:6052`
2. You should see three devices:
   - esp32-garden-zone-a
   - esp32-garden-zone-b (if configured)
   - esp32-utility-control

### Step 4.2: Initial Flash via USB

**Pseudo Code for Zone A:**
```
CONNECT ESP32 to computer via USB
CLICK "Install" on esp32-garden-zone-a
CHOOSE "Plug into this computer"
SELECT serial port
WAIT for compilation and upload
VERIFY successful flash
```

**Steps:**
1. Connect ESP32 to computer with USB cable
2. In ESPHome Dashboard, click "Install" on "esp32-garden-zone-a"
3. Choose "Plug into this computer"
4. Select correct COM/USB port:
   - Windows: COM3, COM4, etc.
   - Linux: /dev/ttyUSB0, /dev/ttyUSB1
   - Mac: /dev/cu.usbserial-*
5. Click "Install"
6. Wait 3-5 minutes for:
   - Firmware compilation
   - Upload to ESP32
   - First boot
7. Check logs for successful connection

**Expected Log Output:**
```
[INFO] OTA successful, restarting...
[INFO] WiFi connected, IP: 192.168.1.50
[INFO] Connected to Home Assistant API
[INFO] Zone A controller started - valve closed
```

### Step 4.3: Verify ESP32 in Home Assistant

**Pseudo Code:**
```
GO TO Home Assistant
NAVIGATE to Settings → Devices & Services
FIND ESP32 device
CHECK entities are available
```

**Steps:**
1. Open Home Assistant
2. Settings → Devices & Services
3. Look for "esp32-garden-zone-a" in Integrations
4. Click the device
5. Verify entities appear:
   - `sensor.zone_a_soil_moisture`
   - `sensor.zone_a_flow_rate`
   - `switch.zone_a_valve`
   - `binary_sensor.zone_a_controller_status`

### Step 4.4: Test Hardware

**Pseudo Code:**
```
FOR EACH sensor:
  VIEW reading in Home Assistant
  VERIFY value is reasonable
  TEST sensor response (change conditions)
END FOR

FOR EACH switch:
  TOGGLE switch in Home Assistant
  VERIFY physical device responds
  CHECK for proper operation
END FOR
```

**Testing Checklist:**

**Soil Moisture Sensor:**
- [ ] Dry reading: 0-20%
- [ ] Moist reading: 40-70%
- [ ] Wet reading: 70-100%
- [ ] Responds to watering

**Flow Sensor:**
- [ ] Zero when water off
- [ ] Increases when water flows
- [ ] Reasonable value (5-20 L/min typical)

**Valve Control:**
- [ ] Click sound when activated
- [ ] Water flows when on
- [ ] Water stops when off
- [ ] No leaks

---

## ⚙️ Phase 5: Calibration

Follow the detailed calibration guide:

```bash
cat docs/CALIBRATION.md
```

**Quick Calibration Steps:**

### 5.1: Calibrate Soil Moisture Sensors

1. Hold sensor in air → note voltage
2. Submerge in water → note voltage
3. Update `esphome/esp32_garden_zone_a.yaml`:
   ```yaml
   - calibrate_linear:
       - 2.85 -> 0.0   # Your dry reading
       - 1.35 -> 100.0 # Your wet reading
   ```
4. Upload updated config via ESPHome Dashboard (OTA)

### 5.2: Calibrate Flow Sensors

1. Run water through sensor
2. Collect exactly 10 liters
3. Count pulses from log
4. Calculate: `pulses_per_liter = total_pulses / 10`
5. Update multiply factor in YAML
6. Upload via OTA

### 5.3: Calibrate Tank Level Sensor

1. Measure tank dimensions
2. Test with empty and full tank
3. Update distances in `esp32_utility_control.yaml`
4. Upload via OTA

---

## 🤖 Phase 6: Automation Configuration

### Step 6.1: Set Input Helpers

**Pseudo Code:**
```
GO TO Home Assistant Settings
SET all input_number values
SET all input_boolean states
SET watering times
```

**Steps:**
1. Settings → Devices & Services → Helpers
2. Set thresholds:
   - **Soil Moisture Low**: 30%
   - **Soil Moisture High**: 70%
   - **Freeze Warning Temp**: 35°F
   - **Rain Skip Threshold**: 0.2 inches
   - **Default Watering Duration**: 15 minutes

3. Enable features:
   - **Master Watering Enable**: ON
   - **Freeze Protection**: ON (March-November)
   - **Leak Detection**: ON

4. Set times:
   - **Morning Watering**: 06:00 AM
   - **Evening Watering**: 07:00 PM (backup)

### Step 6.2: Verify Automations

**Pseudo Code:**
```
GO TO Settings → Automations
VERIFY all automations are enabled
CHECK each automation configuration
TEST trigger conditions
```

**Steps:**
1. Settings → Automations & Scenes
2. Verify these automations exist and are enabled:
   - Morning Watering Schedule
   - Evening Watering Schedule
   - Freeze Protection Activation
   - Leak Detection Emergency Shutoff
   - Low Water Tank Alert
   - Emergency Soil Moisture Watering
   - Daily Weather Report

3. Test automation (safe to test):
   - Click on "Daily Weather Report"
   - Click "Run" (three dots menu)
   - Check your email for report

### Step 6.3: Configure Weather Integration

**Pseudo Code:**
```
VERIFY weather integration is loaded
CHECK weather data is updating
CONFIGURE for Wisconsin zone
TEST weather-based skip logic
```

**Steps:**
1. Developer Tools → States
2. Find `weather.nws_weather`
3. Verify attributes show:
   - Temperature
   - Forecast
   - Precipitation

4. If not working:
   - Check `home-assistant/configuration.yaml`
   - Verify NWS station code for your area
   - Restart Home Assistant

---

## 📊 Phase 7: Monitoring Setup

### Step 7.1: Install Monitoring Script Dependencies

**Pseudo Code:**
```
INSTALL Python packages for monitoring
TEST monitoring script
SCHEDULE with cron
```

**Commands:**
```bash
# Install required packages
pip3 install requests paho-mqtt

# Make script executable
chmod +x scripts/monitor.py

# Test monitoring script (use your HA token)
python3 scripts/monitor.py --ha-token YOUR_LONG_LIVED_TOKEN
```

### Step 7.2: Schedule Automated Monitoring

**Pseudo Code:**
```
ADD cron job for hourly monitoring
LOG results to file
SET up log rotation
```

**Commands:**
```bash
# Edit crontab
crontab -e

# Add this line (replace paths and token):
0 * * * * /usr/bin/python3 /home/pi/projects/Garden-Utility-Automation/scripts/monitor.py --ha-token YOUR_TOKEN --json >> /var/log/garden_monitor.log 2>&1
```

### Step 7.3: Setup Backup Automation

**Pseudo Code:**
```
MAKE backup script executable
TEST backup script
SCHEDULE daily backups
```

**Commands:**
```bash
# Make script executable
chmod +x scripts/backup.sh

# Create backup directory
sudo mkdir -p /backups/garden-automation
sudo chown $USER:$USER /backups/garden-automation

# Test backup
./scripts/backup.sh

# Schedule daily backups at 2 AM
crontab -e

# Add this line:
0 2 * * * /home/pi/projects/Garden-Utility-Automation/scripts/backup.sh >> /var/log/garden_backup.log 2>&1
```

---

## ✅ Phase 8: System Verification

### Step 8.1: End-to-End Test

**Pseudo Code:**
```
MANUALLY trigger watering for one zone
MONITOR sensor readings
VERIFY automation stops watering
CHECK for leaks
REVIEW logs
```

**Test Procedure:**
1. **Prepare:**
   - Ensure tank has adequate water
   - Clear area around test zone
   - Have someone watch for leaks

2. **Execute:**
   - Home Assistant → Developer Tools → Services
   - Call `script.water_zone`
   - Data: `{"zone": "zone_a", "duration": 2}`
   - Click "Call Service"

3. **Observe:**
   - Valve should open (clicking sound)
   - Water should flow
   - Flow sensor should show rate
   - Soil moisture should increase
   - Valve should close after 2 minutes

4. **Verify:**
   - No leaks at any connections
   - Sensors update correctly
   - Logs show no errors

### Step 8.2: Safety System Test

**Test Freeze Protection:**
```yaml
# Temporarily lower freeze threshold for testing
input_number.freeze_warning_temp: 80°F
# Wait for automation to trigger
# Verify watering is disabled
# Reset threshold to 35°F
```

**Test Leak Detection:**
```
# Intentionally cause high flow condition
# (Safely - use a bucket and hose)
# Verify automation triggers
# Verify notification sent
```

### Step 8.3: 24-Hour Soak Test

**Pseudo Code:**
```
RUN system for 24 hours
MONITOR continuously
LOG any issues
VERIFY:
  - ESP32 devices stay connected
  - Sensors update regularly
  - No memory leaks
  - No unexpected reboots
```

**Monitoring:**
```bash
# Watch logs in real-time
docker-compose logs -f --tail=50

# Check ESP32 uptime (should increase)
# Home Assistant → Developer Tools → States
# Search for "uptime" sensors
```

---

## 🎯 Phase 9: Production Deployment

### Step 9.1: Final Configuration

**Pseudo Code:**
```
REVIEW all settings
ENABLE production security
DOCUMENT system configuration
CREATE user manual for family/users
```

**Security Checklist:**
- [ ] Change default passwords
- [ ] Enable MQTT authentication
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS (if remote access needed)
- [ ] Enable Home Assistant 2FA
- [ ] Restrict API access

### Step 9.2: Create System Documentation

**Document:**
- [ ] WiFi credentials location
- [ ] Admin passwords (in secure location)
- [ ] ESP32 IP addresses
- [ ] Sensor locations and labels
- [ ] Valve zone mapping
- [ ] Emergency shutdown procedure
- [ ] Troubleshooting contacts

### Step 9.3: User Training

**Teach users:**
- How to access Home Assistant dashboard
- How to manually control zones
- How to check system status
- How to disable watering (vacation mode)
- Emergency stop procedure
- Who to contact for issues

---

## 🚨 Emergency Procedures

### Total System Shutdown

**Pseudo Code:**
```
1. DISABLE master watering in Home Assistant
2. MANUALLY close all valves
3. DISCONNECT pump power
4. STOP Docker containers (if needed)
```

**Commands:**
```bash
# Stop all watering
# In Home Assistant: Toggle "Master Watering Enable" to OFF

# Stop containers (if needed)
docker-compose down

# Emergency valve close (if HA unavailable)
# Physically disconnect power to relays
```

### Leak Response

**Immediate Actions:**
1. **Close main valve** (if motorized valve installed)
2. **Disable pump**
3. **Inspect system** for leak location
4. **Document damage** (photos)
5. **Repair or call plumber**

### Winter Emergency Shutdown

**If sudden freeze forecast:**
```bash
# Run winterization script
# Home Assistant → Scripts → Winterize System

# Manually drain lines if time permits
# Disconnect water supply
# Open drain valves
```

---

## 📞 Support & Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ESP32 offline | WiFi issue | Check signal strength, verify credentials |
| Sensor shows "unknown" | Wiring issue | Check connections, verify pin assignments |
| Automation not running | Disabled or condition not met | Check automation state, review conditions |
| High water usage | Leak or miscalibration | Check flow sensors, inspect for leaks |
| No watering | Master disabled or weather skip | Check master enable, review weather conditions |

### Log Locations

```bash
# Home Assistant logs
docker-compose logs homeassistant

# MQTT logs
docker-compose logs mqtt

# ESPHome logs (live)
# Access via ESPHome Dashboard → Logs button

# System logs
/var/log/garden_monitor.log
/var/log/garden_backup.log
```

### Getting Help

1. **Check documentation** in `/docs` folder
2. **Review logs** for error messages
3. **Home Assistant Community Forums**: https://community.home-assistant.io/
4. **ESPHome Discord**: https://discord.gg/KhAMKrd
5. **GitHub Issues**: Open issue in repository

---

## ✅ Post-Deployment Checklist

- [ ] All ESP32 devices online and responding
- [ ] All sensors providing valid readings
- [ ] All actuators responding to commands
- [ ] Weather integration working
- [ ] Automations enabled and tested
- [ ] Monitoring script running
- [ ] Backups scheduled and tested
- [ ] Documentation complete
- [ ] Users trained
- [ ] Emergency procedures posted
- [ ] Contact information accessible
- [ ] System labeled and organized

---

**Congratulations!** Your Garden & Utility Automation System is now deployed and operational. 🌱💧

**Remember:** Start with conservative watering schedules and adjust based on plant response and weather patterns.

