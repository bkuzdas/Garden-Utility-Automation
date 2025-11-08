# Contributing to Garden & Utility Automation
### By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas

Thank you for your interest in contributing! This project aims to help gardeners automate their watering systems efficiently.

## 🎯 Contribution Goals

We welcome contributions that:
- Improve documentation clarity
- Add support for new sensors or hardware
- Optimize watering algorithms
- Adapt system for different climates/regions
- Fix bugs or improve stability
- Add new safety features

## 📋 Code Style Requirements

### Pseudo Code Documentation

**All code must include pseudo code comments** explaining the logic:

```yaml
# GOOD EXAMPLE:
################################################################################
# AUTOMATION: Morning Watering
################################################################################
# PSEUDO CODE:
# IF current_time == morning_time THEN:
#   IF master_watering_enabled AND weather_allows_watering THEN:
#     FOR EACH zone:
#       WATER zone
#     END FOR
#   END IF
# END IF
################################################################################
```

### Common Language Explanations

**Include common language explanations for complex concepts:**

```yaml
# COMMON LANGUAGE:
# This automation runs every morning at the time you set. It checks if
# watering is enabled and if the weather is good (no rain, not too cold).
# If conditions are good, it waters each garden zone one by one.
```

## 🐛 Bug Reports

When reporting bugs, please include:
1. **System information** (Home Assistant version, ESP32 board type)
2. **Expected behavior** vs **actual behavior**
3. **Logs** (from Home Assistant, ESPHome, or MQTT)
4. **Configuration** (sanitized - remove passwords!)
5. **Steps to reproduce**

## ✨ Feature Requests

When requesting features:
1. **Describe the use case** (why is this needed?)
2. **Propose a solution** (how should it work?)
3. **Consider compatibility** (will it work for all regions?)
4. **Think about safety** (could it cause flooding or damage?)

## 🔧 Pull Request Process

1. **Fork the repository**: https://github.com/bkuzdas/Garden-Utility-Automation
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
   - Follow existing code style
   - Add pseudo code comments
   - Add common language explanations
   - Test thoroughly
4. **Update documentation**
   - Update README.md if needed
   - Add to CHANGELOG.md
   - Update relevant docs in `/docs`
5. **Commit with clear messages**
   ```
   git commit -m "Add support for DS18B20 temperature sensor
   
   - Added ESP32 config for DS18B20
   - Updated automations to use temperature data
   - Added calibration docs
   - Tested with real hardware"
   ```
6. **Push to your fork**
7. **Open a Pull Request**
   - Describe what you changed and why
   - Reference any related issues
   - Include test results

## 🧪 Testing Requirements

Before submitting:
- [ ] Code validated (YAML syntax, Python syntax)
- [ ] Tested with actual hardware (if hardware changes)
- [ ] No breaking changes (or documented if necessary)
- [ ] Documentation updated
- [ ] Examples provided for new features

## 🌍 Regional Adaptations

If contributing climate-specific adaptations:
- Create a new file: `docs/[REGION]_CLIMATE.md`
- Follow the format of `WISCONSIN_CLIMATE.md`
- Include:
  - Climate statistics
  - Seasonal operating modes
  - Key dates (frost dates, etc.)
  - Regional challenges
  - Recommended thresholds

## 📝 Documentation Standards

- Use clear, simple language
- Include examples
- Add diagrams for complex concepts
- Keep pseudo code updated
- Test all commands/code snippets

## ⚖️ Code of Conduct

- Be respectful and welcoming
- Focus on constructive feedback
- Help newcomers learn
- Keep discussions on-topic
- No harassment or discrimination

## 🙏 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CHANGELOG.md for their contributions
- GitHub contributors page

## 📞 Questions?

Open a GitHub Discussion or Issue if you need help!

Thank you for making garden automation better for everyone! 🌱

