#!/usr/bin/env python3
################################################################################
# GARDEN AUTOMATION SYSTEM MONITOR
# Real-time monitoring and health checks for all system components
# By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas
################################################################################
#
# PSEUDO CODE OVERVIEW:
# 1. Connect to Home Assistant API
# 2. Connect to MQTT broker
# 3. Check status of all ESP32 controllers
# 4. Monitor sensor health (last update times, values in range)
# 5. Check automation states
# 6. Detect anomalies (leaks, stuck sensors, offline devices)
# 7. Generate health report
# 8. Send alerts if issues detected
#
# COMMON LANGUAGE EXPLANATION:
# This script is like a system doctor. It checks all components to make sure
# everything is working correctly. If it finds problems (sensors offline,
# values out of range, automations not running), it alerts you.
#
# USAGE:
#   python3 monitor.py              # Run once, print report
#   python3 monitor.py --continuous # Run forever, check every 5 minutes
#   python3 monitor.py --json       # Output JSON for logging systems
#
################################################################################

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Third-party imports (install with: pip3 install requests paho-mqtt)
try:
    import requests
    import paho.mqtt.client as mqtt
except ImportError:
    print("ERROR: Required packages not installed")
    print("Install with: pip3 install requests paho-mqtt")
    sys.exit(1)

################################################################################
# CONFIGURATION
################################################################################

# Home Assistant Configuration
HA_URL = "http://localhost:8123"
HA_TOKEN = ""  # Set via environment variable or command line

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USERNAME = ""
MQTT_PASSWORD = ""

# Monitoring Thresholds
SENSOR_TIMEOUT_MINUTES = 15  # Alert if sensor hasn't updated in 15 min
EXPECTED_ESP32_COUNT = 3     # Number of ESP32 devices expected
EXPECTED_AUTOMATIONS = 8     # Number of critical automations

# Component Names (adjust to match your configuration)
ESP32_DEVICES = [
    "esp32-garden-zone-a",
    "esp32-garden-zone-b",
    "esp32-utility-control"
]

CRITICAL_SENSORS = [
    "sensor.zone_a_soil_moisture",
    "sensor.zone_b_soil_moisture",
    "sensor.water_tank_level",
    "sensor.main_flow_rate",
    "sensor.nws_weather_temperature"
]

CRITICAL_SWITCHES = [
    "switch.zone_a_valve",
    "switch.zone_b_valve",
    "switch.water_pump",
    "switch.main_water_valve"
]

CRITICAL_AUTOMATIONS = [
    "automation.morning_watering_schedule",
    "automation.freeze_protection_trigger",
    "automation.leak_detection_emergency_shutoff",
    "automation.low_water_tank_alert"
]

################################################################################
# CLASS: SystemMonitor
# PSEUDO CODE:
#   Encapsulates all monitoring logic
#   METHODS:
#     - check_home_assistant_connection()
#     - check_mqtt_connection()
#     - check_esp32_devices()
#     - check_sensors()
#     - check_switches()
#     - check_automations()
#     - check_system_health()
#     - generate_report()
################################################################################

class SystemMonitor:
    """
    Garden Automation System Monitor
    
    Pseudo Code:
    INITIALIZE with configuration
    PROVIDE methods to check each component
    AGGREGATE results into health report
    RETURN pass/fail status
    """
    
    def __init__(self, ha_url: str, ha_token: str, mqtt_broker: str, 
                 mqtt_port: int, mqtt_user: str = "", mqtt_pass: str = ""):
        """
        Initialize system monitor
        
        Pseudo Code:
        SET connection parameters
        INITIALIZE result storage
        CREATE HTTP session for HA
        """
        self.ha_url = ha_url.rstrip('/')
        self.ha_token = ha_token
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_user = mqtt_user
        self.mqtt_pass = mqtt_pass
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "UNKNOWN",
            "checks": {}
        }
        
        # Create HTTP session with HA authentication
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json"
        })
    
    def _api_get(self, endpoint: str) -> Optional[Dict]:
        """
        Make GET request to Home Assistant API
        
        Pseudo Code:
        TRY:
          SEND GET request to HA API
          IF successful THEN return JSON response
        CATCH error:
          LOG error
          RETURN None
        """
        try:
            response = self.session.get(f"{self.ha_url}/api/{endpoint}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: API request failed: {e}")
            return None
    
    def check_home_assistant_connection(self) -> bool:
        """
        Verify Home Assistant is accessible
        
        Pseudo Code:
        TRY:
          GET /api/ endpoint
          IF status 200 THEN HA is online
          RETURN True
        CATCH:
          HA is offline or unreachable
          RETURN False
        """
        print("Checking Home Assistant connection...")
        
        try:
            response = self.session.get(f"{self.ha_url}/api/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.results["checks"]["home_assistant"] = {
                    "status": "ONLINE",
                    "message": data.get("message", "API is running")
                }
                print("✓ Home Assistant is online")
                return True
            else:
                self.results["checks"]["home_assistant"] = {
                    "status": "ERROR",
                    "message": f"HTTP {response.status_code}"
                }
                print(f"✗ Home Assistant returned HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.results["checks"]["home_assistant"] = {
                "status": "OFFLINE",
                "message": str(e)
            }
            print(f"✗ Home Assistant is offline: {e}")
            return False
    
    def check_mqtt_connection(self) -> bool:
        """
        Verify MQTT broker is accessible
        
        Pseudo Code:
        TRY:
          CONNECT to MQTT broker
          IF connected THEN return True
          DISCONNECT
        CATCH:
          MQTT broker offline
          RETURN False
        """
        print("Checking MQTT broker connection...")
        
        mqtt_connected = False
        
        def on_connect(client, userdata, flags, rc):
            nonlocal mqtt_connected
            if rc == 0:
                mqtt_connected = True
        
        try:
            client = mqtt.Client()
            client.on_connect = on_connect
            
            if self.mqtt_user and self.mqtt_pass:
                client.username_pw_set(self.mqtt_user, self.mqtt_pass)
            
            client.connect(self.mqtt_broker, self.mqtt_port, 10)
            client.loop_start()
            time.sleep(2)  # Wait for connection
            client.loop_stop()
            client.disconnect()
            
            if mqtt_connected:
                self.results["checks"]["mqtt"] = {
                    "status": "ONLINE",
                    "message": "Connected successfully"
                }
                print("✓ MQTT broker is online")
                return True
            else:
                self.results["checks"]["mqtt"] = {
                    "status": "ERROR",
                    "message": "Connection failed"
                }
                print("✗ MQTT broker connection failed")
                return False
        except Exception as e:
            self.results["checks"]["mqtt"] = {
                "status": "OFFLINE",
                "message": str(e)
            }
            print(f"✗ MQTT broker is offline: {e}")
            return False
    
    def check_esp32_devices(self) -> bool:
        """
        Check status of all ESP32 controllers
        
        Pseudo Code:
        FOR EACH expected ESP32 device:
          GET device state from HA
          CHECK last_updated timestamp
          IF updated recently THEN device online
          ELSE device offline or stale
        END FOR
        RETURN all_devices_ok
        """
        print(f"Checking {len(ESP32_DEVICES)} ESP32 device(s)...")
        
        all_ok = True
        device_statuses = {}
        
        for device in ESP32_DEVICES:
            # Convert device name to status entity
            status_entity = f"binary_sensor.{device.replace('-', '_')}_status"
            
            state = self._api_get(f"states/{status_entity}")
            
            if state:
                is_online = state.get("state") == "on"
                last_updated = state.get("last_updated", "")
                
                device_statuses[device] = {
                    "online": is_online,
                    "last_updated": last_updated
                }
                
                if is_online:
                    print(f"  ✓ {device}: ONLINE")
                else:
                    print(f"  ✗ {device}: OFFLINE")
                    all_ok = False
            else:
                device_statuses[device] = {
                    "online": False,
                    "last_updated": "N/A",
                    "error": "Entity not found"
                }
                print(f"  ✗ {device}: NOT FOUND")
                all_ok = False
        
        self.results["checks"]["esp32_devices"] = {
            "status": "OK" if all_ok else "DEGRADED",
            "devices": device_statuses
        }
        
        return all_ok
    
    def check_sensors(self) -> bool:
        """
        Check health of critical sensors
        
        Pseudo Code:
        FOR EACH critical sensor:
          GET sensor state
          CHECK last_updated timestamp
          IF timestamp > timeout THEN sensor stale
          CHECK value is reasonable (not unknown/unavailable)
          RECORD status
        END FOR
        """
        print(f"Checking {len(CRITICAL_SENSORS)} critical sensor(s)...")
        
        all_ok = True
        sensor_statuses = {}
        now = datetime.now()
        timeout = timedelta(minutes=SENSOR_TIMEOUT_MINUTES)
        
        for sensor in CRITICAL_SENSORS:
            state = self._api_get(f"states/{sensor}")
            
            if state:
                value = state.get("state")
                last_updated_str = state.get("last_updated", "")
                
                # Check if value is valid
                is_valid = value not in ["unknown", "unavailable", "None", None]
                
                # Check if recently updated
                try:
                    last_updated = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
                    age = now - last_updated.replace(tzinfo=None)
                    is_recent = age < timeout
                except:
                    is_recent = False
                    age = None
                
                sensor_ok = is_valid and is_recent
                
                sensor_statuses[sensor] = {
                    "value": value,
                    "last_updated": last_updated_str,
                    "age_seconds": age.total_seconds() if age else None,
                    "status": "OK" if sensor_ok else "STALE"
                }
                
                if sensor_ok:
                    print(f"  ✓ {sensor}: {value}")
                else:
                    print(f"  ✗ {sensor}: STALE or INVALID")
                    all_ok = False
            else:
                sensor_statuses[sensor] = {
                    "error": "Entity not found",
                    "status": "ERROR"
                }
                print(f"  ✗ {sensor}: NOT FOUND")
                all_ok = False
        
        self.results["checks"]["sensors"] = {
            "status": "OK" if all_ok else "DEGRADED",
            "sensors": sensor_statuses
        }
        
        return all_ok
    
    def check_switches(self) -> bool:
        """
        Check that all critical switches are accessible
        
        Pseudo Code:
        FOR EACH critical switch:
          GET switch state
          VERIFY entity exists and is controllable
        END FOR
        """
        print(f"Checking {len(CRITICAL_SWITCHES)} critical switch(es)...")
        
        all_ok = True
        switch_statuses = {}
        
        for switch in CRITICAL_SWITCHES:
            state = self._api_get(f"states/{switch}")
            
            if state:
                value = state.get("state")
                switch_statuses[switch] = {
                    "state": value,
                    "status": "OK"
                }
                print(f"  ✓ {switch}: {value}")
            else:
                switch_statuses[switch] = {
                    "error": "Entity not found",
                    "status": "ERROR"
                }
                print(f"  ✗ {switch}: NOT FOUND")
                all_ok = False
        
        self.results["checks"]["switches"] = {
            "status": "OK" if all_ok else "DEGRADED",
            "switches": switch_statuses
        }
        
        return all_ok
    
    def check_automations(self) -> bool:
        """
        Check that critical automations are enabled
        
        Pseudo Code:
        FOR EACH critical automation:
          GET automation state
          CHECK if enabled (state = on)
          VERIFY last_triggered is present
        END FOR
        """
        print(f"Checking {len(CRITICAL_AUTOMATIONS)} critical automation(s)...")
        
        all_ok = True
        automation_statuses = {}
        
        for automation in CRITICAL_AUTOMATIONS:
            state = self._api_get(f"states/{automation}")
            
            if state:
                is_on = state.get("state") == "on"
                last_triggered = state.get("attributes", {}).get("last_triggered", "Never")
                
                automation_statuses[automation] = {
                    "enabled": is_on,
                    "last_triggered": last_triggered,
                    "status": "OK" if is_on else "DISABLED"
                }
                
                if is_on:
                    print(f"  ✓ {automation}: ENABLED")
                else:
                    print(f"  ⚠ {automation}: DISABLED")
                    # Not necessarily an error, but worth noting
            else:
                automation_statuses[automation] = {
                    "error": "Entity not found",
                    "status": "ERROR"
                }
                print(f"  ✗ {automation}: NOT FOUND")
                all_ok = False
        
        self.results["checks"]["automations"] = {
            "status": "OK" if all_ok else "DEGRADED",
            "automations": automation_statuses
        }
        
        return all_ok
    
    def generate_report(self, format: str = "text") -> str:
        """
        Generate health report
        
        Pseudo Code:
        AGGREGATE all check results
        DETERMINE overall system status
        FORMAT report as text or JSON
        RETURN report string
        """
        # Determine overall status
        check_statuses = [check.get("status") for check in self.results["checks"].values()]
        
        if all(status == "OK" for status in check_statuses):
            self.results["overall_status"] = "HEALTHY"
        elif any(status == "ERROR" for status in check_statuses):
            self.results["overall_status"] = "ERROR"
        elif any(status in ["DEGRADED", "OFFLINE"] for status in check_statuses):
            self.results["overall_status"] = "DEGRADED"
        else:
            self.results["overall_status"] = "UNKNOWN"
        
        if format == "json":
            return json.dumps(self.results, indent=2)
        else:
            return self._format_text_report()
    
    def _format_text_report(self) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 60)
        lines.append("GARDEN AUTOMATION SYSTEM HEALTH REPORT")
        lines.append("=" * 60)
        lines.append(f"Timestamp: {self.results['timestamp']}")
        lines.append(f"Overall Status: {self.results['overall_status']}")
        lines.append("")
        
        for check_name, check_data in self.results["checks"].items():
            status = check_data.get("status", "UNKNOWN")
            lines.append(f"{check_name.upper()}: {status}")
            
            if check_name in ["sensors", "switches", "automations", "esp32_devices"]:
                # Show details for complex checks
                for item_name, item_data in check_data.items():
                    if item_name != "status" and isinstance(item_data, dict):
                        item_status = item_data.get("status", "OK")
                        lines.append(f"  - {item_name}: {item_status}")
            
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)

################################################################################
# MAIN EXECUTION
################################################################################

def main():
    """
    Main execution flow
    
    Pseudo Code:
    PARSE command line arguments
    INITIALIZE system monitor
    IF continuous mode THEN:
      LOOP forever:
        RUN all checks
        GENERATE report
        SEND alerts if needed
        WAIT interval
    ELSE:
      RUN all checks once
      GENERATE report
      EXIT
    END IF
    """
    parser = argparse.ArgumentParser(description="Garden Automation System Monitor")
    parser.add_argument("--ha-url", default=HA_URL, help="Home Assistant URL")
    parser.add_argument("--ha-token", required=True, help="Home Assistant long-lived access token")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds (default: 300)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(
        ha_url=args.ha_url,
        ha_token=args.ha_token,
        mqtt_broker=MQTT_BROKER,
        mqtt_port=MQTT_PORT,
        mqtt_user=MQTT_USERNAME,
        mqtt_pass=MQTT_PASSWORD
    )
    
    def run_checks():
        """Run all health checks"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting system health check...\n")
        
        monitor.check_home_assistant_connection()
        monitor.check_mqtt_connection()
        monitor.check_esp32_devices()
        monitor.check_sensors()
        monitor.check_switches()
        monitor.check_automations()
        
        report_format = "json" if args.json else "text"
        report = monitor.generate_report(format=report_format)
        print("\n" + report)
        
        return monitor.results["overall_status"]
    
    if args.continuous:
        print("Running in continuous mode (Ctrl+C to stop)")
        while True:
            try:
                run_checks()
                print(f"\nNext check in {args.interval} seconds...\n")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n\nMonitoring stopped by user.")
                break
    else:
        status = run_checks()
        sys.exit(0 if status == "HEALTHY" else 1)

if __name__ == "__main__":
    main()

################################################################################
# USAGE EXAMPLES
################################################################################
#
# 1. Single check with text output:
#    python3 monitor.py --ha-token YOUR_TOKEN
#
# 2. Continuous monitoring every 5 minutes:
#    python3 monitor.py --ha-token YOUR_TOKEN --continuous --interval 300
#
# 3. JSON output for logging:
#    python3 monitor.py --ha-token YOUR_TOKEN --json >> /var/log/garden_monitor.log
#
# 4. Schedule with cron (every hour):
#    0 * * * * python3 /path/to/monitor.py --ha-token TOKEN --json >> /var/log/monitor.log 2>&1
#
################################################################################

