# 📦 GitHub Installation Guide
## How to Install from GitHub Repository
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 🔗 Repository Information

**Official Repository:** https://github.com/bkuzdas/Garden-Utility-Automation

**Clone URL:** 
```
https://github.com/bkuzdas/Garden-Utility-Automation.git
```

---

## 🚀 Quick Installation

### **Method 1: Using HTTPS (Recommended)**

```bash
# Clone the repository
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git

# Navigate into the directory
cd Garden-Utility-Automation

# Verify files are present
ls -la
```

---

### **Method 2: Using SSH (If you have SSH keys configured)**

```bash
# Clone using SSH
git clone git@github.com:bkuzdas/Garden-Utility-Automation.git

# Navigate into the directory
cd Garden-Utility-Automation
```

---

### **Method 3: Download ZIP (No Git required)**

1. **Visit:** https://github.com/bkuzdas/Garden-Utility-Automation
2. **Click:** Green "Code" button
3. **Select:** "Download ZIP"
4. **Extract** the ZIP file to your desired location
5. **Navigate** to the extracted folder

```bash
# After extracting
cd Garden-Utility-Automation-main
```

---

## ✅ Verify Installation

After cloning/downloading, verify you have all the files:

```bash
# Check directory structure
tree -L 2

# Or use ls
ls -la

# You should see:
# - docker-compose.yml
# - env.example
# - README.md
# - START_HERE.md
# - HOW_TO_RUN.md
# - home-assistant/
# - esphome/
# - mqtt/
# - scripts/
# - docs/
```

---

## 🔄 Keeping Updated

### **Update Your Local Copy**

```bash
# Navigate to repository directory
cd Garden-Utility-Automation

# Pull latest changes from GitHub
git pull origin main

# Check what changed
git log --oneline -5
```

### **Check for Updates**

```bash
# See if updates are available
git fetch origin
git status

# If behind, you'll see:
# "Your branch is behind 'origin/main' by X commits"
```

---

## 📋 What You Get

When you clone from GitHub, you receive:

### **Configuration Files**
- ✅ `docker-compose.yml` - Container orchestration
- ✅ `env.example` - Environment template
- ✅ `.gitignore` - Git ignore rules
- ✅ `LICENSE` - MIT License

### **Documentation** (26 files!)
- ✅ `START_HERE.md` - Entry point
- ✅ `HOW_TO_RUN.md` - Running instructions
- ✅ `QUICKSTART.md` - 30-minute setup
- ✅ `README.md` - Project overview
- ✅ `PROJECT_SUMMARY.md` - Complete documentation
- ✅ `docs/DEPLOYMENT.md` - Full deployment guide
- ✅ `docs/CALIBRATION.md` - Sensor calibration
- ✅ `docs/WISCONSIN_CLIMATE.md` - Climate adaptations
- ✅ And more...

### **Home Assistant Configuration**
- ✅ `home-assistant/configuration.yaml`
- ✅ `home-assistant/automations.yaml`
- ✅ `home-assistant/scripts.yaml`
- ✅ `home-assistant/scenes.yaml`
- ✅ `home-assistant/customize.yaml`

### **ESP32 Firmware**
- ✅ `esphome/common/common.yaml`
- ✅ `esphome/esp32_garden_zone_a.yaml`
- ✅ `esphome/esp32_utility_control.yaml`

### **MQTT Configuration**
- ✅ `mqtt/config/mosquitto.conf`

### **Utility Scripts**
- ✅ `scripts/backup.sh` - Automated backups
- ✅ `scripts/monitor.py` - System monitoring

---

## 🎯 Next Steps After Installation

### **1. Read the Documentation**
```bash
# Start with this file
cat START_HERE.md

# Or open in your editor
nano START_HERE.md
```

### **2. Configure Your System**
```bash
# Copy environment template
cp env.example .env

# Edit with your settings
nano .env
```

### **3. Follow Setup Guide**
```bash
# Read the complete running guide
cat HOW_TO_RUN.md

# Or open in browser (if using GUI)
```

---

## 🌐 GitHub Repository Features

### **View Online**
- Browse all files: https://github.com/bkuzdas/Garden-Utility-Automation
- Read documentation in formatted markdown
- View commit history
- Check for updates

### **Report Issues**
- Found a bug? https://github.com/bkuzdas/Garden-Utility-Automation/issues
- Create a new issue with details
- Include logs and error messages

### **Contribute**
- Fork the repository
- Make improvements
- Submit pull requests
- See `CONTRIBUTING.md` for guidelines

---

## 🔐 Security Notes

### **What NOT to Commit**

After configuring, these files contain secrets and should NOT be pushed back to GitHub:

- ❌ `.env` - Your environment variables
- ❌ `home-assistant/secrets.yaml` - Your passwords/API keys
- ❌ `mqtt/config/passwd` - MQTT passwords
- ❌ Any `*.key` or `*.pem` files

**These are already in `.gitignore` for your protection!**

---

## 📊 Repository Structure

```
Garden-Utility-Automation/
├── 📄 Documentation (10+ files)
│   ├── START_HERE.md
│   ├── HOW_TO_RUN.md
│   ├── QUICKSTART.md
│   ├── README.md
│   └── docs/
│       ├── DEPLOYMENT.md
│       ├── CALIBRATION.md
│       └── WISCONSIN_CLIMATE.md
│
├── 🐳 Docker Configuration
│   ├── docker-compose.yml
│   └── env.example
│
├── 🏠 Home Assistant
│   └── home-assistant/
│       ├── configuration.yaml
│       ├── automations.yaml
│       ├── scripts.yaml
│       └── scenes.yaml
│
├── 📡 ESP32 Firmware
│   └── esphome/
│       ├── common/common.yaml
│       ├── esp32_garden_zone_a.yaml
│       └── esp32_utility_control.yaml
│
├── 💬 MQTT Configuration
│   └── mqtt/config/
│       └── mosquitto.conf
│
└── 🔧 Utility Scripts
    └── scripts/
        ├── backup.sh
        └── monitor.py
```

---

## 🆘 Installation Troubleshooting

### **"git: command not found"**

**Install Git:**

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install git

# CentOS/RHEL
sudo yum install git

# macOS
brew install git

# Windows
# Download from: https://git-scm.com/download/win
```

---

### **"Permission denied (publickey)"**

**Solution:** Use HTTPS instead of SSH

```bash
# Use this URL
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git

# Instead of
git clone git@github.com:bkuzdas/Garden-Utility-Automation.git
```

---

### **"Repository not found"**

**Check:**
1. URL is correct: `https://github.com/bkuzdas/Garden-Utility-Automation.git`
2. Repository is public (it should be)
3. Your internet connection is working

---

### **"fatal: destination path already exists"**

**Solution:** Directory already exists

```bash
# Either remove it
rm -rf Garden-Utility-Automation

# Or use a different name
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git Garden-Utility-Automation-new
```

---

## 🎓 Git Basics

### **Check Repository Status**
```bash
cd Garden-Utility-Automation
git status
```

### **View Commit History**
```bash
git log --oneline
```

### **See What Changed**
```bash
git diff
```

### **Discard Local Changes**
```bash
# Discard all changes
git reset --hard

# Or discard specific file
git checkout -- filename
```

---

## 📞 Support

### **Installation Help**
- GitHub Repository: https://github.com/bkuzdas/Garden-Utility-Automation
- GitHub Issues: https://github.com/bkuzdas/Garden-Utility-Automation/issues
- Documentation: See `START_HERE.md` after cloning

### **Git Help**
- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/

---

## ✅ Installation Checklist

After following this guide:

- [ ] Git installed on your system
- [ ] Repository cloned to local machine
- [ ] All files present (verify with `ls -la`)
- [ ] Read `START_HERE.md`
- [ ] Ready to follow `HOW_TO_RUN.md`

---

## 🎉 Successfully Installed!

**Your next steps:**

1. ✅ **Installation complete** (you are here)
2. 📍 **Read:** `START_HERE.md` for navigation
3. 🚀 **Follow:** `HOW_TO_RUN.md` to start the system
4. 🌱 **Enjoy:** Automated gardening!

---

**Garden & Utility Automation System**  
**By Brian Kuzdas - 03/02/2024**  
**Repository:** https://github.com/bkuzdas/Garden-Utility-Automation

