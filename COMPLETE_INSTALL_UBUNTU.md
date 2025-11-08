# 🐧 Complete Installation Guide for Ubuntu 22.04
## From Fresh Ubuntu Install to Running Garden Automation
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 📍 **Overview**

This guide takes you from a **fresh Ubuntu 22.04 installation** to a **fully running Garden Automation System** with every single step documented.

**Time Required:** 45-60 minutes  
**Skill Level:** Beginner-friendly with copy-paste commands  
**What You'll Install:** Docker, Docker Compose, Garden Automation System

---

## ✅ **Prerequisites**

- **Ubuntu 22.04 LTS** (Desktop or Server)
- **Internet connection**
- **sudo privileges** (ability to run admin commands)
- **Keyboard and monitor** (or SSH access)

---

## 📋 **What We'll Do (Step by Step)**

```
1. Update Ubuntu system
2. Install Git
3. Install Docker Engine
4. Install Docker Compose
5. Configure Docker permissions
6. Clone Garden Automation repository
7. Configure the system
8. Start Docker containers
9. Access Home Assistant
10. Verify everything works
```

---

## 🚀 **PHASE 1: Prepare Ubuntu System**

### **Step 1.1: Update System Packages**

**Pseudo Code:**
```
UPDATE package list from repositories
UPGRADE all installed packages to latest versions
REBOOT if kernel was updated
```

**Commands:**
```bash
# Update package list
sudo apt update

# Upgrade all packages (this may take 5-10 minutes)
sudo apt upgrade -y

# Check if reboot is needed
if [ -f /var/run/reboot-required ]; then
  echo "Reboot required! Run: sudo reboot"
fi
```

**What this does:**
- Updates the list of available packages
- Installs the latest versions of all software
- Shows if you need to reboot (if kernel updated)

**Output you should see:**
```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
...
Reading package lists... Done
Building dependency tree... Done
...
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

---

### **Step 1.2: Install Required Tools**

**Pseudo Code:**
```
INSTALL curl (for downloading files)
INSTALL git (for cloning repository)
INSTALL nano (text editor)
```

**Commands:**
```bash
# Install essential tools
sudo apt install -y curl git nano ca-certificates gnupg lsb-release

# Verify installation
curl --version
git --version
nano --version
```

**What this does:**
- `curl` - Downloads files from the internet
- `git` - Version control system for cloning repositories
- `nano` - Simple text editor
- `ca-certificates` - SSL certificates for secure connections

**Expected output:**
```
curl 7.81.0 (x86_64-pc-linux-gnu)
git version 2.34.1
GNU nano, version 6.2
```

---

## 🐳 **PHASE 2: Install Docker**

### **Step 2.1: Install Docker Engine**

**Pseudo Code:**
```
DOWNLOAD Docker installation script from official source
RUN installation script
VERIFY Docker is installed correctly
```

**Commands:**
```bash
# Download Docker installation script
curl -fsSL https://get.docker.com -o get-docker.sh

# Review the script (optional but recommended)
cat get-docker.sh

# Run the installation script
sudo sh get-docker.sh

# Verify Docker is installed
docker --version
```

**What this does:**
- Downloads official Docker installation script
- Automatically detects Ubuntu 22.04 and installs correct version
- Sets up Docker Engine, CLI, and containerd

**Expected output:**
```
# Executing docker install script, commit: a8e8c69
+ sudo -E sh -c apt-get update -qq >/dev/null
+ sudo -E sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin >/dev/null
...
Client: Docker Engine - Community
 Version:           24.0.7
```

---

### **Step 2.2: Install Docker Compose**

**Pseudo Code:**
```
INSTALL docker-compose from Ubuntu repositories
VERIFY docker-compose is working
CHECK version number
```

**Commands:**
```bash
# Install Docker Compose
sudo apt install -y docker-compose

# Verify installation
docker-compose --version
```

**Expected output:**
```
docker-compose version 1.29.2, build unknown
```

**Note:** Ubuntu 22.04 includes Docker Compose v1. This is fine for our project!

---

### **Step 2.3: Configure Docker Permissions**

**Pseudo Code:**
```
ADD current user to docker group
LOG OUT and back in to apply changes
TEST docker without sudo
```

**Commands:**
```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Check it was added
groups $USER

# Apply the group change (choose ONE method)

# Method 1: Log out and back in (RECOMMENDED)
# Just close your terminal and open a new one

# Method 2: Apply immediately without logout
newgrp docker

# Method 3: Reboot
# sudo reboot
```

**What this does:**
- Adds your user to the "docker" group
- Allows you to run `docker` commands without `sudo`
- **IMPORTANT:** You MUST log out and back in for this to work!

**Test it works:**
```bash
# This should work WITHOUT sudo
docker ps

# Expected output:
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

---

### **Step 2.4: Enable Docker to Start on Boot**

**Pseudo Code:**
```
CONFIGURE Docker to start automatically when system boots
VERIFY Docker service is enabled
```

**Commands:**
```bash
# Enable Docker service
sudo systemctl enable docker

# Start Docker service now
sudo systemctl start docker

# Check Docker status
sudo systemctl status docker
```

**Expected output:**
```
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since ...
```

Press `q` to exit the status view.

---

## 📥 **PHASE 3: Download Garden Automation**

### **Step 3.1: Create Project Directory**

**Pseudo Code:**
```
CREATE a directory for projects
NAVIGATE into that directory
```

**Commands:**
```bash
# Create projects folder in your home directory
mkdir -p ~/projects

# Navigate to it
cd ~/projects

# Verify where you are
pwd
```

**Expected output:**
```
/home/yourusername/projects
```

---

### **Step 3.2: Clone Repository from GitHub**

**Pseudo Code:**
```
CLONE Garden Automation repository from GitHub
NAVIGATE into the project directory
LIST files to verify download
```

**Commands:**
```bash
# Clone the repository
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git

# Navigate into it
cd Garden-Utility-Automation

# List all files
ls -la

# See the structure
tree -L 2  # Or just: ls -R
```

**Expected output:**
```
Cloning into 'Garden-Utility-Automation'...
remote: Enumerating objects: 150, done.
remote: Counting objects: 100% (150/150), done.
remote: Compressing objects: 100% (100/100), done.
remote: Total 150 (delta 50), reused 150 (delta 50), pack-reused 0
Receiving objects: 100% (150/150), 250.00 KiB | 5.00 MiB/s, done.
Resolving deltas: 100% (50/50), done.
```

**Verify files are present:**
```bash
ls -la
# You should see:
# docker-compose.yml
# env.example
# README.md
# home-assistant/
# esphome/
# mqtt/
# scripts/
# docs/
```

---

## ⚙️ **PHASE 4: Configure the System**

### **Step 4.1: Create Environment File**

**Pseudo Code:**
```
COPY the example environment file
EDIT it with your specific settings
```

**Commands:**
```bash
# Copy the template
cp env.example .env

# Open it in nano text editor
nano .env
```

**What to change in the file:**

1. **Find these lines and change them:**

```bash
# Your WiFi (for ESP32 devices)
WIFI_SSID=YourActualWiFiName          # ← Change this
WIFI_PASSWORD=YourActualWiFiPassword   # ← Change this

# Your location (find on Google Maps)
LATITUDE=43.0731   # ← Change to your latitude
LONGITUDE=-89.4012 # ← Change to your longitude

# Security passwords (CHANGE THESE!)
MQTT_PASSWORD=ChangeThisPassword123    # ← Change this
ESPHOME_OTA_PASSWORD=ChangeOTAPass456  # ← Change this
```

2. **Save the file:**
   - Press `Ctrl + X`
   - Press `Y` (yes to save)
   - Press `Enter` (confirm filename)

**How to find your coordinates:**
1. Go to Google Maps
2. Right-click your location
3. Click the coordinates (they'll copy)
4. Paste into the .env file

---

### **Step 4.2: Create Home Assistant Secrets File**

**Pseudo Code:**
```
COPY the secrets template
EDIT it with your passwords and API keys
```

**Commands:**
```bash
# Copy the template
cp home-assistant/secrets.yaml.example home-assistant/secrets.yaml

# Edit it
nano home-assistant/secrets.yaml
```

**What to change:**

```yaml
# Location (use same as .env file)
latitude: 43.0731      # ← Your latitude
longitude: -89.4012    # ← Your longitude
elevation: 259         # ← Your elevation in meters

# MQTT (use same password as .env)
mqtt_username: "garden_mqtt_user"
mqtt_password: "ChangeThisPassword123"  # ← Same as .env

# Weather (optional - can leave default)
nws_station: "KMSN"  # Find yours at weather.gov
```

**Save:** `Ctrl + X`, `Y`, `Enter`

---

### **Step 4.3: Create Required Directories**

**Pseudo Code:**
```
CREATE directories for MQTT data and logs
SET proper permissions
```

**Commands:**
```bash
# Create MQTT directories
mkdir -p mqtt/data mqtt/log

# Set permissions (allows Docker to write)
chmod 777 mqtt/data mqtt/log

# Verify directories exist
ls -la mqtt/
```

**Expected output:**
```
drwxrwxrwx  2 user user 4096 ... data
drwxrwxrwx  2 user user 4096 ... log
```

---

## 🚀 **PHASE 5: Start the System**

### **Step 5.1: Start Docker Containers**

**Pseudo Code:**
```
START all Docker containers in background mode
WAIT for them to initialize
CHECK if they're running
```

**Commands:**
```bash
# Start all containers
docker-compose up -d

# Wait 30 seconds for initialization
sleep 30

# Check status
docker-compose ps
```

**Expected output:**
```
Creating network "garden-utility-automation_default" with the default driver
Creating volume "garden-utility-automation_esphome" with default driver
Pulling homeassistant (homeassistant/home-assistant:stable)...
...
Creating garden_mqtt_broker ... done
Creating garden_esphome_dashboard ... done
Creating garden_homeassistant ... done
```

**Check they're running:**
```bash
docker-compose ps

# Should show:
NAME                       STATE    PORTS
garden_homeassistant       Up       
garden_mqtt_broker         Up       1883/tcp, 9001/tcp
garden_esphome_dashboard   Up       6052/tcp
```

---

### **Step 5.2: View Logs (Optional but Recommended)**

**Pseudo Code:**
```
VIEW container logs to verify no errors
CHECK for successful startup messages
```

**Commands:**
```bash
# View all logs
docker-compose logs

# View logs for specific service
docker-compose logs homeassistant

# Follow logs live (press Ctrl+C to stop)
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50
```

**Look for these success messages:**
```
homeassistant    | INFO (MainThread) [homeassistant.core] Starting Home Assistant
mqtt             | 1234567890: mosquitto version 2.0.18 running
esphome          | INFO Starting dashboard web server on ...
```

---

## 🌐 **PHASE 6: Access Home Assistant**

### **Step 6.1: Find Your Server's IP Address**

**Pseudo Code:**
```
FIND the IP address of your Ubuntu machine
NOTE it down for accessing from browser
```

**Commands:**
```bash
# Method 1: Using hostname command
hostname -I

# Method 2: Using ip command
ip addr show | grep "inet " | grep -v 127.0.0.1

# Method 3: If using WiFi
ip addr show wlan0 | grep "inet "
```

**Expected output:**
```
192.168.1.100  # This is your IP address
```

**Note this down!** You'll need it in the next step.

---

### **Step 6.2: Open Home Assistant in Browser**

**Pseudo Code:**
```
OPEN web browser
NAVIGATE to Home Assistant URL
COMPLETE onboarding wizard
```

**Steps:**

1. **Open a web browser** (Firefox, Chrome, etc.)

2. **Go to this URL** (replace with your IP):
   ```
   http://192.168.1.100:8123
   ```
   
   Or if on the same machine:
   ```
   http://localhost:8123
   ```

3. **Wait 1-2 minutes** for Home Assistant to fully start (first time)

4. **You should see:** Home Assistant onboarding screen

---

### **Step 6.3: Complete Home Assistant Setup**

**Pseudo Code:**
```
CREATE admin account
SET name and location
SKIP integrations for now
FINISH setup
```

**Steps:**

1. **Create Your Account:**
   - Name: `Your Name`
   - Username: `admin` (or your choice)
   - Password: `Strong password here`
   - Confirm password
   - Click "Create Account"

2. **Name Your Home:**
   - Home name: `Garden Automation`
   - Location: Should auto-detect or use your coordinates
   - Click "Next"

3. **Share Data:**
   - Choose your preference
   - Click "Next"

4. **Set Up Integrations:**
   - Click "Skip" (we'll set up later)

5. **Finish:**
   - Click "Finish"

6. **You're in!** You should see the Home Assistant dashboard

---

## ✅ **PHASE 7: Verify Installation**

### **Step 7.1: Check All Services Are Running**

**Commands:**
```bash
# Check Docker containers
docker-compose ps

# All should show "Up"
```

### **Step 7.2: Test Each Service**

**1. Home Assistant:**
```
Browser: http://YOUR_IP:8123
Should show: Home Assistant dashboard
```

**2. ESPHome Dashboard:**
```
Browser: http://YOUR_IP:6052
Should show: ESPHome dashboard with your device configs
```

**3. MQTT Broker:**
```bash
# Check MQTT logs
docker-compose logs mqtt | grep "mosquitto version"

# Should show: mosquitto version X.X.X running
```

---

### **Step 7.3: Run System Health Check**

**Commands:**
```bash
# Check all containers are running
docker-compose ps | grep "Up"

# Check Home Assistant is responding
curl -s http://localhost:8123 | grep -q "Home Assistant"
echo $?  # Should output: 0 (means success)

# Check disk space
df -h

# Check memory
free -h
```

**All checks passed?** ✅ Your system is running!

---

## 📊 **What You Now Have Running**

| Service | URL | Purpose |
|---------|-----|---------|
| **Home Assistant** | http://YOUR_IP:8123 | Main automation dashboard |
| **ESPHome** | http://YOUR_IP:6052 | ESP32 firmware management |
| **MQTT Broker** | mqtt://YOUR_IP:1883 | Message broker (no web UI) |

---

## 🎯 **Next Steps**

Now that your system is running, you can:

### **Immediate:**
- ✅ Explore Home Assistant dashboard
- ✅ Check out the ESPHome dashboard
- ✅ Read `HOW_TO_RUN.md` for next steps

### **With Hardware:**
1. Connect ESP32 devices via USB
2. Flash firmware using ESPHome Dashboard
3. Test sensors and valves
4. Calibrate sensors (see `docs/CALIBRATION.md`)

### **Configuration:**
1. Set up automations
2. Configure watering schedules
3. Set thresholds
4. Enable notifications

---

## 🔧 **Troubleshooting**

### **Problem: "docker: command not found"**

**Solution:**
```bash
# Docker not installed properly, try again
sudo sh get-docker.sh

# Or install manually
sudo apt install -y docker.io docker-compose
```

---

### **Problem: "Permission denied" when running docker**

**Solution:**
```bash
# Add yourself to docker group again
sudo usermod -aG docker $USER

# MUST log out and back in!
# Or run:
newgrp docker

# Test
docker ps
```

---

### **Problem: "Cannot connect to Home Assistant"**

**Solution:**
```bash
# Check containers are running
docker-compose ps

# If not running, start them
docker-compose up -d

# Check logs for errors
docker-compose logs homeassistant

# Check firewall (if enabled)
sudo ufw status
sudo ufw allow 8123/tcp  # Allow Home Assistant
```

---

### **Problem: "Container exited with error"**

**Solution:**
```bash
# View logs to see what went wrong
docker-compose logs

# Common issue: Port already in use
sudo lsof -i :8123  # Check what's using port 8123

# Fix: Stop the conflicting service or change port
```

---

### **Problem: "Cannot access from other computers"**

**Solution:**
```bash
# Check Ubuntu firewall
sudo ufw status

# If active, allow the ports
sudo ufw allow 8123/tcp  # Home Assistant
sudo ufw allow 6052/tcp  # ESPHome
sudo ufw allow 1883/tcp  # MQTT

# Check you're using the correct IP
ip addr show
```

---

## 📋 **Complete Installation Checklist**

After following this guide, check that you have:

- [ ] Ubuntu 22.04 updated and upgraded
- [ ] Git installed and working
- [ ] Docker Engine installed and running
- [ ] Docker Compose installed
- [ ] User added to docker group (can run without sudo)
- [ ] Repository cloned to `~/projects/Garden-Utility-Automation`
- [ ] `.env` file created and configured
- [ ] `secrets.yaml` file created and configured
- [ ] All Docker containers running (`docker-compose ps` shows "Up")
- [ ] Home Assistant accessible in browser (port 8123)
- [ ] ESPHome Dashboard accessible in browser (port 6052)
- [ ] No errors in container logs

**All checked?** 🎉 **Your Garden Automation System is installed and running!**

---

## 💾 **Important: Make a Backup**

Now that everything is working, make a backup:

```bash
# Create backup directory
mkdir -p ~/backups

# Backup your configuration
cd ~/projects/Garden-Utility-Automation
tar -czf ~/backups/garden-automation-$(date +%Y%m%d).tar.gz \
  .env \
  home-assistant/secrets.yaml \
  home-assistant/configuration.yaml \
  esphome/

# Verify backup was created
ls -lh ~/backups/
```

---

## 🔄 **Managing Your System**

### **Start/Stop/Restart:**
```bash
cd ~/projects/Garden-Utility-Automation

# Stop everything
docker-compose stop

# Start everything
docker-compose start

# Restart everything
docker-compose restart

# Stop and remove containers (data is preserved)
docker-compose down

# Start fresh
docker-compose up -d
```

### **View Logs:**
```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f homeassistant
```

### **Update System:**
```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose up -d
```

---

## 📞 **Getting Help**

If you run into issues:

1. **Check logs:** `docker-compose logs`
2. **Check this guide's troubleshooting section** (above)
3. **Read:** `HOW_TO_RUN.md` for more details
4. **GitHub Issues:** https://github.com/bkuzdas/Garden-Utility-Automation/issues
5. **Community:** Home Assistant forums

---

## 🎓 **Understanding What You Installed**

### **Docker Containers:**
- **homeassistant**: The brain - handles automation logic
- **mqtt**: The messenger - carries messages between devices
- **esphome**: The programmer - manages ESP32 firmware

### **Why Docker:**
- Easy to install (no dependency hell)
- Easy to update (just pull new images)
- Easy to backup (copy config files)
- Isolated (won't mess up your Ubuntu)

### **File Locations:**
```
~/projects/Garden-Utility-Automation/
├── home-assistant/    ← Home Assistant config
├── esphome/          ← ESP32 firmware configs
├── mqtt/             ← MQTT broker data
└── .env              ← Your settings (KEEP PRIVATE!)
```

---

## ✨ **Congratulations!**

You've successfully installed the Garden Automation System on Ubuntu 22.04!

**What you learned:**
- ✅ How to update Ubuntu
- ✅ How to install Docker and Docker Compose
- ✅ How to clone from GitHub
- ✅ How to configure environment files
- ✅ How to start and manage Docker containers
- ✅ How to access web services
- ✅ How to troubleshoot common issues

**Your system is now ready for:**
- Adding ESP32 hardware
- Configuring automations
- Setting up sensors
- Automated garden watering!

---

**Next Step:** Open `HOW_TO_RUN.md` for what to do next! 🚀🌱

---

**Garden & Utility Automation System**  
**By Brian Kuzdas - 03/02/2024**  
**Complete Ubuntu Installation Guide**  
**Repository:** https://github.com/bkuzdas/Garden-Utility-Automation

