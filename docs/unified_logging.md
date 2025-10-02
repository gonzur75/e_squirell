# Unified Logging System

This document describes the unified logging system implemented across all components of the E-Squirell project.

## Overview

The E-Squirell project now uses a unified logging system that provides consistent logging across all components:
- Backend (Django)
- ESP32 devices
- MQTT communication

The system ensures that logs from all components have a consistent format, are properly categorized by component and log level, and can be easily aggregated and analyzed.

## Components

### Backend Logging

The backend uses Python's standard logging module with a custom JSON formatter. The configuration is loaded from a TOML file.

Key files:
- `backend/config/logging_/config.py` - Main configuration loader
- `backend/config/logging_/config.toml` - Logging configuration
- `backend/config/logging_/unified_logger.py` - Unified logging implementation

#### Usage

```python
from config.logging_.config import get_unified_logger

# Get a logger for your module
logger = get_unified_logger(__name__)

# Log messages at different levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### ESP32 Logging

The ESP32 devices use a custom logging implementation that mimics Python's standard logging module. It supports logging to both the console and MQTT.

Key files:
- `esp32_soft/logging.py` - ESP32 logging implementation

#### Usage

```python
from logging import get_logger

# Get a logger for your module
logger = get_logger("module_name")

# Log messages at different levels
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Log an exception and optionally restart the device
logger.exception(error, "Error message", restart=True)
```

### MQTT Logging Integration

The MQTT client in the backend receives logs from ESP32 devices and integrates them into the backend logging system.

Key files:
- `backend/storage_heater/helpers/mqtt_client.py` - MQTT client with logging integration

## Log Levels

The unified logging system uses the following log levels, consistent with Python's standard logging module:

| Level | Value | Description |
|-------|-------|-------------|
| DEBUG | 10 | Detailed information, typically of interest only when diagnosing problems |
| INFO | 20 | Confirmation that things are working as expected |
| WARNING | 30 | An indication that something unexpected happened, or may happen in the near future |
| ERROR | 40 | Due to a more serious problem, the software has not been able to perform some function |
| CRITICAL | 50 | A serious error, indicating that the program itself may be unable to continue running |

## Log Format

Logs are formatted as JSON objects with the following fields:

```json
{
  "timestamp": "2023-01-01T12:00:00+00:00",
  "level": "INFO",
  "message": "Log message",
  "component": "backend",
  "module": "module_name",
  "function": "function_name",
  "line": 123,
  "thread_name": "MainThread"
}
```

## Configuration

### Backend Configuration

The backend logging configuration is defined in `backend/config/logging_/config.toml`. This file specifies:
- Log formatters (simple and JSON)
- Log handlers (console and file)
- Logger configurations

### ESP32 Configuration

The ESP32 logging is configured when initializing the logging system:

```python
from logging import setup_logging

# Set up logging with MQTT integration
logger = setup_logging(mqtt_client=client, mqtt_topic=topic)
```

## Best Practices

1. **Use the appropriate log level** for each message:
   - DEBUG for detailed diagnostic information
   - INFO for general operational information
   - WARNING for unexpected but non-critical issues
   - ERROR for errors that prevent normal operation
   - CRITICAL for severe errors that require immediate attention

2. **Include context in log messages** to make them more useful:
   - What operation was being performed
   - What data was being processed
   - What the expected outcome was

3. **Structure log messages consistently** to make them easier to parse and analyze

4. **Use exception logging** for errors to capture stack traces

5. **Include component information** to identify the source of logs in a distributed system