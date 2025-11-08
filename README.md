# Garden and Utility Automation System
## Midwest Wisconsin Climate-Optimized Smart Irrigation & Utility Management
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 🌱 Project Overview

This Garden and Utility Automation project establishes a robust, two-tiered control system using Docker containers for centralized management and ESP32 microcontrollers for local hardware interfacing.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER HOST SERVER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Home         │  │ MQTT         │  │ ESPHome      │      │
│  │ Assistant    │←→│ Broker       │←→│ Dashboard    │      │
│  │ (Core Logic) │  │ (Messaging)  │  │ (OTA Updates)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           ↕ (WiFi/MQTT/ESPHome API)
┌─────────────────────────────────────────────────────────────┐
│              ESP32 EDGE CONTROLLERS (Physical Layer)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ESP32 #1     │  │ ESP32 #2     │  │ ESP32 #3     │      │
│  │ Garden Zone A│  │ Garden Zone B│  │ Utility      │      │
│  │              │  │              │  │ Management   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           ↕ (GPIO Pins)
┌─────────────────────────────────────────────────────────────┐
│                  SENSORS & ACTUATORS                         │
│  • Capacitive Soil Moisture Sensors                         │
│  • Water Level Sensors (Tank Protection)                    │
│  • Flow Sensors (Usage Tracking & Leak Detection)           │
│  • Solenoid Water Valves (Zone Control)                     │
│  • Relay Modules (Pump Control)                             │
│  • Motorized Ball Valves (Emergency Shutoff)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features

### 1. **Weather-Intelligent Irrigation**
- **Predictive Logic**: Skips watering when rain is forecast
- **Wind Adaptation**: Adjusts schedules based on wind speed
- **Temperature-Based**: Modifies watering duration for Wisconsin seasons
- **Water Conservation**: Only waters when soil moisture is below threshold

### 2. **Multi-Zone Garden Control**
- Independent zones for different plant types
- Customizable moisture thresholds per zone
- Flow monitoring for each zone
- Emergency shutoff capabilities

### 3. **Utility Management**
- Automated pump control for reservoir systems
- Leak detection with automatic main water shutoff
- Water level monitoring and alerts
- Usage tracking and reporting

### 4. **Safety Features**
- Freeze protection (critical for Wisconsin winters)
- Tank overflow prevention
- Leak detection and automatic isolation
- Pump dry-run protection

---

## 📋 Hardware Requirements

### Central Server (Docker Host)
- **Recommended**: Raspberry Pi 4 (4GB+) or x86 Linux server
- **Storage**: 32GB+ SD card/SSD
- **Network**: Ethernet connection (preferred for stability)
- **OS**: Debian-based Linux (Ubuntu, Raspberry Pi OS)

### ESP32 Controllers (Per Zone)
- **Model**: ESP32-DevKitC or ESP32-WROOM-32
- **Power**: 5V 2A power supply per ESP32
- **Quantity**: 2-4 units depending on zone count

### Sensors
| Sensor Type | Quantity | Purpose | Notes |
|-------------|----------|---------|-------|
| Capacitive Soil Moisture | 2-8 | Per zone monitoring | Corrosion-resistant |
| Water Flow Sensor | 1-4 | Usage tracking | YF-S201 or similar |
| Water Level Sensor | 1-2 | Tank monitoring | Ultrasonic or float |
| DHT22/BME280 | 1-2 | Local temp/humidity | Optional but useful |

### Actuators
| Actuator Type | Quantity | Purpose | Notes |
|---------------|----------|---------|-------|
| 12V Solenoid Valve | 2-8 | Zone control | NC (Normally Closed) |
| Relay Module (5V) | 2-6 | Switch control | Optocoupled |
| Water Pump | 1-2 | Reservoir transfer | 12V DC or 120V AC |
| Motorized Ball Valve | 1 | Main shutoff | Optional, 12V |

### Additional Hardware
- **Wire**: 18-22 AWG for sensors, 14-16 AWG for valves
- **Power Supplies**: 12V 5A for valves/pump
- **Enclosures**: Waterproof IP65+ for outdoor installations
- **Connectors**: Waterproof cable glands

---

## 🚀 Quick Start Guide

**→ See `HOW_TO_RUN.md` for complete step-by-step running instructions**

### Prerequisites
```bash
# Required software on Docker host
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
```

### Installation Steps

#### 1. Clone Repository
```bash
git clone https://github.com/bkuzdas/Garden-Utility-Automation.git
cd Garden-Utility-Automation
```

#### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

#### 3. Start Docker Containers
```bash
# Build and start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### 4. Access Services
- **Home Assistant**: http://localhost:8123
- **ESPHome Dashboard**: http://localhost:6052
- **MQTT Broker**: localhost:1883

#### 5. Flash ESP32 Devices
1. Open ESPHome Dashboard
2. Connect ESP32 via USB
3. Click "Install" on desired configuration
4. Choose "Plug into this computer"
5. After first flash, subsequent updates are OTA

---

## 🌦️ Weather API Configuration

This system supports multiple weather providers for Wisconsin:

### Recommended: National Weather Service (NWS) - FREE
- No API key required
- Excellent for US locations
- Provides forecasts and alerts

### Alternative: OpenWeatherMap
- Free tier: 1000 calls/day
- Get API key: https://openweathermap.org/api

### Configuration in Home Assistant
See `home-assistant/configuration.yaml` for setup details.

---

## 📂 Project Structure

```
Garden-Utility-Automation/
├── docker-compose.yml              # Main orchestration file
├── .env.example                    # Environment template
├── README.md                       # This file
│
├── docs/                           # Documentation
│   ├── HARDWARE_SETUP.md          # Wiring diagrams
│   ├── CALIBRATION.md             # Sensor calibration
│   ├── TROUBLESHOOTING.md         # Common issues
│   └── WISCONSIN_CLIMATE.md       # Regional considerations
│
├── home-assistant/                 # HA configuration
│   ├── configuration.yaml         # Main HA config
│   ├── automations.yaml           # Automation rules
│   ├── scripts.yaml               # Reusable scripts
│   ├── secrets.yaml.example       # Secrets template
│   └── packages/
│       ├── garden_zones.yaml      # Zone definitions
│       ├── weather_logic.yaml     # Weather automations
│       └── utility_control.yaml   # Pump/valve control
│
├── esphome/                        # ESP32 configurations
│   ├── common/
│   │   ├── common.yaml            # Shared settings
│   │   └── sensors.yaml           # Reusable sensors
│   ├── esp32_garden_zone_a.yaml   # Zone A controller
│   ├── esp32_garden_zone_b.yaml   # Zone B controller
│   └── esp32_utility_control.yaml # Utility controller
│
├── scripts/                        # Utility scripts
│   ├── backup.sh                  # Backup automation
│   ├── monitor.py                 # System monitoring
│   └── calibrate_sensors.py       # Sensor calibration
│
└── diagrams/                       # Wiring diagrams
    ├── esp32_pinout.png
    ├── valve_wiring.png
    └── complete_system.png
```

---

## 🔒 Security Considerations

1. **Change Default Passwords**: Update all default credentials
2. **Network Isolation**: Consider VLAN for IoT devices
3. **MQTT Authentication**: Enable username/password on broker
4. **Home Assistant**: Enable multi-factor authentication
5. **Firewall**: Do not expose services to internet without VPN
6. **Backups**: Automated backups configured in docker-compose

---

## 🌡️ Wisconsin Climate Adaptations

### Spring (March-May)
- **Challenge**: Unpredictable freezes
- **Adaptation**: Frost protection automation, delayed spring startup
- **Watering**: Moderate, watch for late frosts

### Summer (June-August)
- **Challenge**: Hot, humid, occasional drought
- **Adaptation**: Peak watering season, humidity-adjusted schedules
- **Watering**: Heavy, morning schedules to reduce fungal issues

### Fall (September-November)
- **Challenge**: Rapid temperature drops
- **Adaptation**: Gradual watering reduction, winterization prep
- **Watering**: Decreasing, prepare for shutdown

### Winter (December-February)
- **Challenge**: Freezing temperatures, snow
- **Adaptation**: System hibernation, pipe drainage
- **Watering**: System offline, monitoring only

---

## 📊 Monitoring & Alerts

### Built-in Dashboards
- Real-time soil moisture by zone
- Water usage statistics
- Weather forecast integration
- System health status

### Alert Notifications
- Low water tank levels
- High flow rate (leak detection)
- Sensor offline warnings
- Freeze warnings
- Pump failures

### Notification Options
- Mobile app (Home Assistant Companion)
- Email
- SMS (via integrations)
- Push notifications

---

## 🛠️ Maintenance Schedule

### Daily (Automated)
- ✅ Sensor health checks
- ✅ Weather data refresh
- ✅ Log file rotation

### Weekly
- 🔍 Visual inspection of valves/connections
- 🔍 Check soil moisture sensor accuracy
- 🔍 Review water usage reports

### Monthly
- 🔧 Clean filters
- 🔧 Inspect for leaks
- 🔧 Calibrate flow sensors

### Seasonal
- 🔧 Spring: System startup, check for winter damage
- 🔧 Summer: Peak season inspection
- 🔧 Fall: Prepare for winterization
- 🔧 Winter: Drain system, monitor for freezes

---

## 🤝 Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🆘 Support

- **Documentation**: Check `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/bkuzdas/Garden-Utility-Automation/issues)
- **Repository**: https://github.com/bkuzdas/Garden-Utility-Automation
- **Community**: Home Assistant Community Forums

---

## 🙏 Acknowledgments

- Home Assistant Community
- ESPHome Project
- Eclipse Mosquitto (MQTT)
- Wisconsin Gardening Community

---

**Made with ❤️ for sustainable Midwest gardening**

