# Wisconsin Climate Considerations
## Garden Automation Adaptations for Midwest Gardening
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

---

## 🌡️ Climate Overview

Wisconsin has a **continental climate** with four distinct seasons and significant temperature extremes. Successful garden automation must adapt to these conditions.

### Climate Statistics (Madison, WI area)

| Season | Temp Range | Precipitation | Key Challenges |
|--------|------------|---------------|----------------|
| **Winter** (Dec-Feb) | -10°F to 30°F | 8" (mostly snow) | Freezing, system hibernation |
| **Spring** (Mar-May) | 25°F to 70°F | 10" | Unpredictable frosts, mud |
| **Summer** (Jun-Aug) | 55°F to 85°F | 12" | Heat waves, humidity, storms |
| **Fall** (Sep-Nov) | 30°F to 65°F | 9" | Early frosts, rapid cooling |

**Annual Total:** ~35-40 inches precipitation

---

## ❄️ Winter Operations (December - February)

### System Status: **HIBERNATION MODE**

**Pseudo Code Logic:**
```
WHEN month IN [December, January, February]:
  DISABLE all watering operations
  CLOSE all valves
  TURN OFF pump
  ENABLE freeze_protection mode
  DRAIN all exposed water lines
  MONITOR temperature only
END WHEN
```

**Common Language:**
The system essentially sleeps through winter. All watering is disabled, and the focus shifts entirely to preventing freeze damage.

### Critical Winterization Steps

#### 1. System Shutdown (Late November)

**Checklist:**
- [ ] Disable master watering in Home Assistant
- [ ] Close all zone valves
- [ ] Turn off pump
- [ ] Disconnect water supply to system
- [ ] Open all drain valves
- [ ] Blow out lines with compressed air (20-30 PSI max)
- [ ] Remove and store any outdoor sensors susceptible to freeze
- [ ] Insulate any components that must remain in place
- [ ] Apply heat tape to vulnerable pipes in crawl spaces

#### 2. ESP32 Winter Configuration

**Pseudo Code:**
```
DURING winter months:
  DISABLE watering automations
  MAINTAIN ESP32 connectivity for:
    - Freeze monitoring
    - System status checks
    - Spring startup readiness
  LOG temperature data for planning
```

**Implementation:**
Add to Home Assistant automations:

```yaml
- id: winter_mode_activation
  alias: "Activate Winter Mode"
  trigger:
    - platform: time
      at: "00:00:00"
  condition:
    - condition: template
      value_template: "{{ now().month in [12, 1, 2] }}"
  action:
    - service: input_boolean.turn_off
      target:
        entity_id: input_boolean.master_watering_enable
    - service: script.winterize_system
```

#### 3. Wisconsin Winter Hazards

| Hazard | Risk | Prevention |
|--------|------|------------|
| **Pipe Freezing** | Burst pipes, system destruction | Drain all lines, insulate, heat tape |
| **Sensor Damage** | Cracked housings, failed electronics | Remove or insulate sensors |
| **Valve Seizure** | Valves stuck closed in spring | Cycle valves before final shutdown |
| **Snow Load** | Crushed equipment | Protect/shelter outdoor components |
| **Ice Dams** | Water infiltration | Weatherproof all electrical enclosures |

### Temperature Monitoring

**Pseudo Code:**
```
EVEN during winter:
  MONITOR outdoor temperature
  IF temperature > 40°F for 7+ consecutive days THEN:
    ALERT: Possible early spring, prepare for startup
  END IF
  
  IF temperature < -10°F THEN:
    ALERT: Extreme cold, check insulation and heat tape
  END IF
```

---

## 🌱 Spring Operations (March - May)

### System Status: **GRADUAL ACTIVATION**

**Pseudo Code Logic:**
```
SPRING_STARTUP_CRITERIA:
  average_temperature > 40°F for 7 days
  AND last_frost_date passed (typically May 1-15)
  AND soil_temperature > 45°F
  
THEN:
  INSPECT system for winter damage
  RESTORE water supply gradually
  TEST each zone individually
  ENABLE watering with conservative schedules
```

**Common Language:**
Spring in Wisconsin is tricky—warm days can lure you into starting too early, then a late frost hits. The automation must be conservative and frost-aware.

### Spring Startup Procedure

#### 1. Pre-Startup Inspection (Late April)

**Checklist:**
- [ ] Visual inspection of all pipes for cracks
- [ ] Check valve operation manually
- [ ] Verify ESP32 connectivity
- [ ] Test sensors for accuracy
- [ ] Clear any debris from sensors/valves
- [ ] Check pump for ice damage
- [ ] Verify weatherproofing still intact

#### 2. Gradual System Activation

**Pseudo Code:**
```
STARTUP_SEQUENCE:
  1. RESTORE water supply slowly (prevent water hammer)
  2. CHECK for leaks with low pressure
  3. TEST each zone for 30 seconds only
  4. VERIFY no leaks detected
  5. ENABLE leak detection automation
  6. ENABLE freeze protection (still needed!)
  7. SET conservative watering schedule
  8. MONITOR closely for first 2 weeks
```

#### 3. Frost Protection Automation

**Critical for Wisconsin Springs!**

**Pseudo Code:**
```
EVERY evening (March 15 - May 31):
  CHECK overnight temperature forecast
  IF forecast_low < 35°F THEN:
    CANCEL morning watering schedule
    SEND notification: "Frost warning - watering skipped"
    ENABLE frost protection mode
  END IF
```

**Implementation:**
```yaml
- id: spring_frost_protection
  alias: "Spring Frost Protection"
  trigger:
    - platform: time
      at: "18:00:00"
  condition:
    - condition: template
      value_template: "{{ now().month in [3, 4, 5] }}"
    - condition: numeric_state
      entity_id: sensor.nws_weather_temperature_forecast_low
      below: 35
  action:
    - service: input_boolean.turn_off
      target:
        entity_id: input_boolean.master_watering_enable
    - service: notify.email
      data:
        title: "❄️ Frost Warning Tonight"
        message: "Temperature forecast: {{ states('sensor.nws_weather_temperature_forecast_low') }}°F. Watering disabled."
```

### Spring Challenges

| Challenge | Impact | Automation Response |
|-----------|--------|---------------------|
| **Late Frost** (May) | Kills tender plants | Skip watering if temp < 35°F |
| **Heavy Rain** | Flooding, erosion | Monitor rain accumulation, skip watering |
| **Mud Season** | Waterlogged soil | Extend dry-out periods between watering |
| **Rapid Temperature Swings** | Stress plants | Gradual watering schedule increases |

### Recommended Spring Schedule

**Pseudo Code:**
```
MARCH: System offline, monitoring only
APRIL 1-15: System testing, no automatic watering
APRIL 15-30: Manual watering only, frost monitoring active
MAY 1-15: Automatic watering enabled, conservative schedule
MAY 15+: Normal summer schedule (if no frost for 7 days)
```

---

## ☀️ Summer Operations (June - August)

### System Status: **FULL OPERATION**

**Pseudo Code Logic:**
```
SUMMER is peak watering season
IMPLEMENT smart watering:
  ADJUST for temperature
  ADJUST for humidity
  SKIP if thunderstorms forecast
  WATER in morning to reduce fungal issues
  MONITOR for drought stress
```

**Common Language:**
Summer is when the system really shines. Wisconsin summers can be humid and hot, with occasional drought periods. The automation must balance water conservation with plant health.

### Wisconsin Summer Characteristics

#### Heat & Humidity

**Typical Conditions:**
- Daytime: 75-85°F (heat waves: 90-100°F)
- Humidity: 60-80%
- Dew Point: Often 60-70°F (sticky!)

**Automation Adaptations:**

**Pseudo Code:**
```
CALCULATE heat_stress_factor:
  IF temperature > 85°F AND humidity > 70% THEN:
    heat_stress = HIGH
    INCREASE watering duration by 30%
    RECOMMEND morning watering only (reduce fungal risk)
  ELSE IF temperature > 90°F THEN:
    heat_stress = EXTREME
    INCREASE watering duration by 50%
    CONSIDER second evening watering session
  ELSE:
    heat_stress = NORMAL
    USE standard watering duration
  END IF
```

#### Thunderstorms

**Common Language:**
Wisconsin summer thunderstorms can dump 1-2 inches of rain in an hour! The system must skip watering when these are forecast.

**Pseudo Code:**
```
EVERY morning at 05:00:
  CHECK weather forecast for next 12 hours
  IF rain_probability > 60% THEN:
    SKIP morning watering
  END IF
  
  IF rain_accumulation_forecast > 0.5 inches THEN:
    SKIP morning watering
    DISABLE watering for 24-48 hours
  END IF
```

**Implementation:**
```yaml
sensor:
  - platform: template
    sensors:
      skip_watering_today:
        value_template: >
          {% set rain = state_attr('weather.nws_weather', 'forecast')[0].precipitation | float(0) %}
          {% set rain_prob = state_attr('weather.nws_weather', 'forecast')[0].precipitation_probability | int(0) %}
          {{ rain > 0.5 or rain_prob > 60 }}
```

### Summer Watering Schedule

**Optimal Times:**
- **Morning**: 5:00-8:00 AM (BEST - reduces fungal diseases)
- **Evening**: 7:00-9:00 PM (OK - use if morning watering insufficient)
- **Midday**: NEVER (wasteful due to evaporation, can burn leaves)

**Pseudo Code:**
```
RECOMMENDED_SCHEDULE:
  Monday, Wednesday, Friday: Morning watering
  Tuesday, Thursday, Saturday: Check soil moisture
    IF moisture < 30% THEN evening watering
  Sunday: No watering (rest day, soil assessment)
```

### Drought Management

**Wisconsin Drought Patterns:**
- Typically late July - early August
- Can last 2-4 weeks
- May have watering restrictions in some municipalities

**Pseudo Code:**
```
DURING drought conditions:
  PRIORITIZE zones:
    Priority 1: Vegetable garden (daily)
    Priority 2: Flower beds (every 2 days)
    Priority 3: Lawn (weekly or skip)
  
  INCREASE watering duration
  DECREASE watering frequency
  (Deep, infrequent watering promotes root depth)
  
  MONITOR soil moisture closely
  ALERT if any zone critically dry
```

---

## 🍂 Fall Operations (September - November)

### System Status: **GRADUAL SHUTDOWN**

**Pseudo Code Logic:**
```
FALL_OPERATIONS:
  September: Normal watering, watch for early frost
  October: Reduce watering frequency, prepare for shutdown
  November: Final shutdown before freeze
  
  WHEN first_frost_date_forecast THEN:
    BEGIN winterization_procedure
  END WHEN
```

**Common Language:**
Fall is about gradually reducing watering as plants go dormant and preparing the system for winter shutdown.

### Fall Watering Adjustments

**Pseudo Code:**
```
SEPTEMBER:
  watering_duration = summer_duration * 0.8
  watering_frequency = 3x per week

OCTOBER:
  watering_duration = summer_duration * 0.5
  watering_frequency = 1-2x per week
  
  IF temperature < 40°F THEN:
    DISABLE watering
  END IF

NOVEMBER:
  watering = DISABLED
  INITIATE winterization
```

### First Frost Monitoring

**Critical Dates:**
- Average first frost: **September 25 - October 10**
- Can occur as early as September 15
- Killing frost (< 28°F): October 15-30

**Automation:**
```yaml
- id: first_frost_warning
  alias: "First Frost Warning"
  trigger:
    - platform: numeric_state
      entity_id: sensor.nws_weather_temperature_forecast_low
      below: 32
  condition:
    - condition: template
      value_template: "{{ now().month in [9, 10, 11] }}"
  action:
    - service: notify.email
      data:
        title: "❄️ First Frost Warning"
        message: "First frost forecast. Consider harvesting tender vegetables and beginning winterization."
```

### Winterization Trigger

**Pseudo Code:**
```
WINTERIZATION_CRITERIA:
  (forecast_low < 32°F within 7 days)
  OR (date == November 15)
  OR (manual_trigger == TRUE)

THEN:
  RUN script.winterize_system
  SEND winterization checklist
  DISABLE all watering automations until spring
```

---

## 🌧️ Wisconsin Precipitation Patterns

### Monthly Rainfall Averages

| Month | Avg. Rainfall | Irrigation Needs |
|-------|---------------|------------------|
| January | 1.3" | None (frozen) |
| February | 1.1" | None (frozen) |
| March | 2.1" | None (too cold) |
| April | 3.4" | Low (cool, wet) |
| May | 3.6" | Moderate |
| June | 4.1" | Moderate-High |
| July | 3.9" | High (evaporation) |
| August | 4.2" | High (evaporation) |
| September | 3.6" | Moderate |
| October | 2.5" | Low |
| November | 2.2" | None |
| December | 1.7" | None (frozen) |

### Smart Water Conservation

**Pseudo Code:**
```
WATER_CONSERVATION_LOGIC:
  IF recent_rain_7days > 2 inches THEN:
    SKIP watering for 5-7 days
  ELSE IF recent_rain_3days > 1 inch THEN:
    SKIP watering for 2-3 days
  ELSE IF rain_forecast_today > 0.5 inches THEN:
    SKIP today's watering
  ELSE:
    PROCEED with schedule
  END IF
```

---

## 📊 Home Assistant Weather Integration Settings

### National Weather Service (NWS) Configuration

**For Wisconsin (Madison area example):**

```yaml
weather:
  - platform: nws
    api_key: your_api_key
    station: KMSN  # Madison
    # Other major stations:
    # KMKE - Milwaukee
    # KGRB - Green Bay
    # KLSE - La Crosse
    # KEAU - Eau Claire
    mode: daynight
```

### Wisconsin Weather Zones

Find your zone at: https://www.weather.gov/

**Example Zones:**
- **WIZ063**: Dane County (Madison)
- **WIZ066**: Milwaukee County
- **WIZ040**: Green Bay area
- **WIZ041**: Door County

---

## 🎯 Season-Specific Automation Parameters

### Recommended Threshold Settings by Season

**Spring (Apr-May):**
```yaml
soil_moisture_threshold: 40%  # Keep soil moist, not wet
watering_duration: 10 minutes
freeze_warning_temp: 35°F
rain_skip_threshold: 0.3 inches
max_daily_waterings: 1
```

**Summer (Jun-Aug):**
```yaml
soil_moisture_threshold: 30%  # Allow more drying
watering_duration: 15-20 minutes
heat_adjustment: enabled (above 85°F)
rain_skip_threshold: 0.5 inches
max_daily_waterings: 2 (if heat > 90°F)
```

**Fall (Sep-Oct):**
```yaml
soil_moisture_threshold: 35%
watering_duration: 8 minutes
freeze_warning_temp: 35°F
rain_skip_threshold: 0.2 inches
max_daily_waterings: 1
```

---

## ✅ Wisconsin-Specific Automation Checklist

- [ ] Freeze protection automation enabled (March-May, September-November)
- [ ] Frost forecast monitoring configured
- [ ] Winterization procedure documented and tested
- [ ] Spring startup procedure created
- [ ] Heat stress adjustment algorithm configured
- [ ] Thunderstorm rain skip logic enabled
- [ ] Drought management priorities set
- [ ] First frost alert configured
- [ ] NWS weather integration with correct station
- [ ] Seasonal schedule changes automated
- [ ] All exposed components winterized or protected
- [ ] Heat tape and insulation installed where needed

---

## 📞 Wisconsin Gardening Resources

- **UW-Madison Extension**: https://hort.extension.wisc.edu/
- **Wisconsin State Climatology Office**: https://www.aos.wisc.edu/~sco/
- **National Weather Service - Milwaukee**: https://www.weather.gov/mkx/
- **Wisconsin Gardening Calendar**: Plan plantings and maintenance

---

**Remember:** Wisconsin's climate requires careful attention to seasonal transitions. The automation system must be equally smart about when NOT to water as when to water!

