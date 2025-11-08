# Sensor Calibration Guide
## Garden & Utility Automation System
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 📐 Overview

This guide explains how to calibrate all sensors in your garden automation system for accurate readings. Proper calibration is **critical** for efficient water usage and reliable system operation.

---

## 🌱 Capacitive Soil Moisture Sensors

### Why Calibration is Needed

**Pseudo Code Logic:**
```
SENSOR reads capacitance of surrounding material
CAPACITANCE varies with:
  - Soil type (clay, sand, loam)
  - Soil temperature
  - Mineral content
  - Sensor manufacturing variance

RAW_VALUE must be mapped to PERCENTAGE (0-100%)
WITHOUT calibration, readings are meaningless numbers
```

**Common Language:**
Soil moisture sensors measure electrical properties of the soil, which change with water content. However, different soils and different sensors give different numbers for the same wetness level. Calibration tells the system "this number means dry, that number means wet."

### Calibration Process

#### Step 1: Prepare Your Sensor
1. **Clean the sensor**: Remove any dirt or corrosion
2. **Connect to ESP32**: Wire to the designated GPIO pin (see wiring diagram)
3. **Power on ESP32**: Ensure it's connected to Home Assistant

#### Step 2: Get "Dry" Reading (0% Moisture)

**Pseudo Code:**
```
PLACE sensor in completely dry medium (air)
WAIT 2 minutes for reading to stabilize
READ raw ADC value
RECORD as DRY_VALUE
```

**Steps:**
1. Hold sensor in open air (or in completely dry soil)
2. Navigate to ESPHome Dashboard: `http://your-ip:6052`
3. Click "Logs" on your zone controller
4. Find the line showing `"Zone A Soil Moisture Raw"`
5. Record the **voltage value** (typically 2.7-3.0V for dry)
6. Example: `[sensor:127]: 'Zone A Soil Moisture Raw': Got voltage=2.85V`
7. **Write down: DRY_VALUE = 2.85**

#### Step 3: Get "Wet" Reading (100% Moisture)

**Pseudo Code:**
```
SUBMERGE sensor in water (not the electronics!)
WAIT 2 minutes for reading to stabilize
READ raw ADC value
RECORD as WET_VALUE
```

**Steps:**
1. Fill a glass with water
2. Submerge **only the probe portion** (not the electronics!) into water
3. Wait 2 minutes
4. Check ESPHome logs again
5. Record the voltage value (typically 1.2-1.5V for wet)
6. Example: `[sensor:127]: 'Zone A Soil Moisture Raw': Got voltage=1.35V`
7. **Write down: WET_VALUE = 1.35**

#### Step 4: Update Configuration

**Pseudo Code:**
```
IN esphome/esp32_garden_zone_a.yaml:
  FIND calibrate_linear section
  UPDATE values:
    DRY_VALUE -> 0.0
    WET_VALUE -> 100.0
```

**Steps:**
1. Open `esphome/esp32_garden_zone_a.yaml`
2. Find the calibration section:

```yaml
- calibrate_linear:
    - 2.8 -> 0.0   # Replace 2.8 with your DRY_VALUE
    - 1.3 -> 100.0 # Replace 1.3 with your WET_VALUE
```

3. Replace with your values:

```yaml
- calibrate_linear:
    - 2.85 -> 0.0   # Your recorded dry reading
    - 1.35 -> 100.0 # Your recorded wet reading
```

4. Save the file
5. In ESPHome Dashboard, click "Upload" (OTA update)
6. Wait for upload to complete (~2 minutes)

#### Step 5: Verify Calibration

**Pseudo Code:**
```
TEST sensor in various conditions
CHECK that readings make sense:
  Air: ~0%
  Water: ~100%
  Moist soil: 30-70%
  Dry soil: 0-20%
```

**Steps:**
1. Hold sensor in air → Should read ~0-5%
2. Submerge in water → Should read ~95-100%
3. Place in actual soil → Should read reasonable value
4. Water the soil → Value should increase
5. Let soil dry → Value should decrease

### Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| Reading always 0% | Sensor disconnected | Check wiring |
| Reading always 100% | Short circuit | Check for wire damage |
| Reading fluctuates wildly | Electrical noise | Add longer averaging window |
| Reading doesn't change | Sensor failed | Replace sensor |
| Backwards reading | Inverted calibration | Swap dry/wet values |

---

## 💧 Water Flow Sensors

### Why Calibration is Needed

**Pseudo Code Logic:**
```
FLOW SENSOR generates pulses as water flows
PULSE_FREQUENCY proportional to FLOW_RATE
CALIBRATION_FACTOR converts pulses to liters

flow_rate (L/min) = pulses_per_minute / CALIBRATION_FACTOR
```

**Common Language:**
Flow sensors have a little turbine that spins with water flow. Each rotation generates electrical pulses. The number of pulses per liter of water varies by sensor model and water pressure. Calibration ensures accurate volume measurement.

### Calibration Process

#### Method 1: Known Volume Test (Most Accurate)

**Pseudo Code:**
```
FLOW known volume of water through sensor
COUNT total pulses
CALCULATE: pulses_per_liter = total_pulses / volume_liters
UPDATE calibration factor in ESP32 config
```

**Steps:**
1. Connect sensor to water supply and ESP32
2. Prepare a bucket and measuring jug
3. Open ESPHome logs to see pulse counts
4. **Record starting pulse count** (e.g., "Total Water Used: 0.0 L")
5. Run water through sensor into bucket
6. Collect exactly **10 liters** of water (use measuring jug)
7. **Record ending pulse count** (e.g., "Total: 4500 pulses")
8. Calculate: `pulses_per_liter = 4500 / 10 = 450`

#### Method 2: Use Manufacturer Specification

**Common Flow Sensor Calibrations:**

| Sensor Model | Pulses per Liter | Multiply Factor for ESPHome |
|--------------|------------------|------------------------------|
| YF-S201 | 450 | 0.00222 |
| YF-S402 | 5880 | 0.00017 |
| YF-DN40 | 1980 | 0.000505 |
| Hall Effect Generic | 660 | 0.001515 |

**Pseudo Code:**
```
LOOKUP sensor model specification
FIND pulses_per_liter
CALCULATE multiply_factor = 1 / pulses_per_liter
```

#### Update Configuration

**Pseudo Code:**
```
IN ESP32 config:
  FIND pulse_counter section for flow sensor
  FIND filters: multiply
  UPDATE multiply value
```

**Steps:**
1. Open your ESP32 YAML file
2. Find the flow sensor section:

```yaml
- platform: pulse_counter
  pin: GPIO25
  name: "Zone A Flow Rate"
  filters:
    - multiply: 0.1333  # <-- Update this value
```

3. Calculate new multiply factor:
   - If you measured 450 pulses/liter: `multiply = 1/450 = 0.00222`
   - For flow rate in L/min: `multiply = 60/450 = 0.1333`

4. Update both locations (flow rate and total):

```yaml
# For flow rate (L/min)
filters:
  - multiply: 0.1333  # Your calculated value

# For total volume (L)
total:
  filters:
    - multiply: 0.00222  # Your calculated value
```

5. Upload updated configuration

#### Verification

**Pseudo Code:**
```
RUN water through system
MEASURE actual volume dispensed
COMPARE to sensor reading
ERROR_PERCENT = |actual - measured| / actual * 100
IF ERROR_PERCENT > 5% THEN recalibrate
```

**Steps:**
1. Reset total water counter in Home Assistant
2. Run a zone for exactly 10 minutes
3. Measure actual water dispensed (use bucket and measuring jug)
4. Compare to sensor reading
5. If difference > 5%, adjust calibration factor:
   - `new_factor = old_factor * (actual_volume / sensor_reading)`

---

## 📏 Ultrasonic Water Level Sensor

### Why Calibration is Needed

**Pseudo Code Logic:**
```
ULTRASONIC SENSOR measures distance to water surface
DISTANCE must be converted to TANK_LEVEL percentage

tank_level% = (tank_height - current_distance) / tank_height * 100

REQUIRES knowing:
  - Total tank height
  - Sensor mounting height
  - Offset when tank is "full" (water below sensor)
```

**Common Language:**
The ultrasonic sensor shoots sound waves down and measures how long they take to bounce back. This tells us the distance to the water. We need to convert this distance into a percentage (0% = empty, 100% = full) based on your specific tank dimensions.

### Calibration Process

#### Step 1: Measure Tank Dimensions

**Required Measurements:**

1. **Tank Height**: Measure from bottom to top (inside measurement)
   - Example: 100 cm

2. **Sensor Height**: Measure from sensor to tank bottom
   - Example: 105 cm (sensor is 5 cm above top of tank)

3. **Full Level Distance**: Distance from sensor to water when tank is "full"
   - Tanks are never filled to the brim
   - Example: 10 cm (water is 10 cm below sensor when "full")

4. **Empty Level Distance**: Distance from sensor to tank bottom
   - Example: 105 cm

#### Step 2: Calculate Values

**Pseudo Code:**
```
tank_height = sensor_height_from_bottom
sensor_to_full = distance_to_water_when_full
sensor_to_empty = distance_to_tank_bottom
usable_height = sensor_to_empty - sensor_to_full
```

**Example Calculation:**
- Tank height: 100 cm
- Sensor mounted 5 cm above tank: 105 cm from bottom
- Water level when "full": 10 cm from sensor
- Water level when "empty": 105 cm from sensor
- Usable range: 105 - 10 = 95 cm

#### Step 3: Test with Known Levels

**Pseudo Code:**
```
FOR EACH test_level IN [empty, half, full]:
  SET tank to test_level
  MEASURE actual water depth
  READ sensor distance
  CALCULATE expected percentage
  COMPARE to sensor reading
  IF error > 5% THEN adjust calibration
END FOR
```

**Steps:**
1. **Empty Tank Test**:
   - Drain tank completely
   - Sensor should read maximum distance (~105 cm)
   - Calculated level should be ~0%

2. **Half Full Test**:
   - Fill tank to known midpoint
   - Calculate expected distance
   - Verify sensor reading matches

3. **Full Tank Test**:
   - Fill tank to normal "full" level
   - Sensor should read minimum distance (~10 cm)
   - Calculated level should be ~100%

#### Step 4: Update Configuration

**Pseudo Code:**
```
IN esp32_utility_control.yaml:
  FIND water tank level template sensor
  UPDATE calibration constants:
    tank_height = your_tank_height
    sensor_to_full = your_distance_when_full
    sensor_to_empty = your_distance_when_empty
```

**Steps:**
1. Open `esphome/esp32_utility_control.yaml`
2. Find the tank level calculation:

```yaml
lambda: |-
  // CALIBRATION VALUES - Adjust for your tank
  float tank_height = 1.00;        // Update: Tank height in meters
  float sensor_to_full = 0.10;     // Update: Distance when tank full
  float sensor_to_empty = 0.98;    // Update: Distance when tank empty
```

3. Convert your measurements to meters and update:

```yaml
lambda: |-
  float tank_height = 1.05;        // Your tank: 105 cm = 1.05 m
  float sensor_to_full = 0.10;     // Your measurement: 10 cm = 0.10 m
  float sensor_to_empty = 1.05;    // Your measurement: 105 cm = 1.05 m
```

4. Upload configuration

### Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Reading always 100% | Sensor too close to water | Remount higher |
| Reading always 0% | Distance out of range | Check max_range setting |
| Erratic readings | Water surface ripples | Increase averaging window |
| No reading | Wiring issue | Check trigger/echo pins |

---

## 🔧 General Calibration Best Practices

### Environmental Considerations

**Pseudo Code Logic:**
```
SENSORS affected by environmental factors:
  Temperature: affects capacitance and distance measurements
  Humidity: affects soil readings
  Pressure: affects flow measurements
  
RECOMMENDATION: Calibrate under typical operating conditions
```

**Common Language:**
- Calibrate sensors in the conditions they'll actually work in
- For soil sensors: calibrate with your actual garden soil, not potting mix
- For flow sensors: calibrate at typical water pressure
- For level sensors: account for temperature effects on sound speed

### Maintenance Schedule

| Sensor Type | Recalibration Frequency | Reason |
|-------------|------------------------|---------|
| Soil Moisture | Annually (spring) | Sensor degradation, soil changes |
| Flow Sensors | Semi-annually | Scale buildup, wear |
| Level Sensors | Annually | Mounting shift, sensor drift |

### Documentation

**After calibrating each sensor, document:**

1. **Date of calibration**
2. **Calibration values used**
3. **Environmental conditions** (temperature, etc.)
4. **Test results** (actual vs measured)
5. **Sensor serial number** (if available)

**Create a calibration log file:**

```
Calibration Log - Garden Automation System

===========================================
Date: 2024-04-15
Sensor: Zone A Soil Moisture
Location: Vegetable Garden, North Bed
Technician: Your Name

Dry Reading (air): 2.85V → 0%
Wet Reading (water): 1.35V → 100%
Test in soil: 1.95V → 56% (reasonable)

Status: ✅ Calibrated Successfully
===========================================
```

---

## 🎯 Calibration Validation Checklist

Before putting your system into production, verify:

- [ ] All soil moisture sensors read 0-10% in air
- [ ] All soil moisture sensors read 90-100% in water
- [ ] All soil moisture sensors give reasonable readings (20-70%) in actual soil
- [ ] Flow sensors accurately measure known volumes (within 5%)
- [ ] Flow rate readings match expected values during operation
- [ ] Tank level sensor reads 0% when empty
- [ ] Tank level sensor reads 100% when full
- [ ] All sensors update at expected intervals
- [ ] No sensor readings show "unknown" or "unavailable"
- [ ] All calibration values documented

---

## 📞 Support

If you're having calibration issues:

1. Check ESPHome logs for sensor readings
2. Verify wiring against pinout diagrams
3. Test with known reference values
4. Check Home Assistant forums for sensor-specific advice
5. Consider sensor replacement if consistent failures

---

**Remember:** Good calibration is the foundation of accurate automation! Take your time and document everything.

