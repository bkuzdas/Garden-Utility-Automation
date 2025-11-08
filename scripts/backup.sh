#!/bin/bash
################################################################################
# GARDEN AUTOMATION BACKUP SCRIPT
# Automated backup of all system configurations
# By Brian Kuzdas - 03/02/2024 - Copyright (c) 2024 Brian Kuzdas
################################################################################
#
# PSEUDO CODE LOGIC:
# 1. Create timestamped backup directory
# 2. Backup Home Assistant configuration files
# 3. Backup ESPHome configurations
# 4. Backup MQTT configuration
# 5. Backup database (if using external DB)
# 6. Compress backup into archive
# 7. Retain only last N backups (configurable)
# 8. Optional: Upload to remote storage
#
# COMMON LANGUAGE EXPLANATION:
# This script makes a complete snapshot of your garden automation system.
# It's like taking a photo of all your settings so you can restore them
# if something goes wrong. Run this regularly (daily recommended).
#
# USAGE:
#   ./scripts/backup.sh
#
# SCHEDULE WITH CRON:
#   0 2 * * * /path/to/scripts/backup.sh >> /var/log/garden_backup.log 2>&1
#   (Runs every day at 2 AM)
#
################################################################################

# CONFIGURATION VARIABLES
# Common Language: Set these to match your setup

# Where to store backups
BACKUP_ROOT="/backups/garden-automation"

# Number of backups to keep (older ones deleted)
RETENTION_DAYS=30

# Source directories
HOME_ASSISTANT_DIR="./home-assistant"
ESPHOME_DIR="./esphome"
MQTT_DIR="./mqtt"
SCRIPTS_DIR="./scripts"

# Backup filename pattern
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="garden_automation_backup_${TIMESTAMP}"
BACKUP_DIR="${BACKUP_ROOT}/${BACKUP_NAME}"

# Colors for output (makes logs readable)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

################################################################################
# FUNCTION: log_message
# PSEUDO CODE:
#   INPUT: message, level (INFO/WARN/ERROR)
#   OUTPUT: Formatted log message with timestamp
################################################################################
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # PSEUDO CODE: Color code by severity
    case $level in
        "INFO")
            echo -e "${GREEN}[${timestamp}] [INFO]${NC} ${message}"
            ;;
        "WARN")
            echo -e "${YELLOW}[${timestamp}] [WARN]${NC} ${message}"
            ;;
        "ERROR")
            echo -e "${RED}[${timestamp}] [ERROR]${NC} ${message}"
            ;;
        *)
            echo "[${timestamp}] ${message}"
            ;;
    esac
}

################################################################################
# FUNCTION: check_prerequisites
# PSEUDO CODE:
#   CHECK if required tools are installed (tar, gzip, etc.)
#   IF missing THEN exit with error
################################################################################
check_prerequisites() {
    log_message "INFO" "Checking prerequisites..."
    
    # PSEUDO CODE: Verify required commands exist
    local required_commands=("tar" "gzip" "date")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            log_message "ERROR" "Required command not found: $cmd"
            return 1
        fi
    done
    
    log_message "INFO" "All prerequisites met"
    return 0
}

################################################################################
# FUNCTION: create_backup_directory
# PSEUDO CODE:
#   CREATE timestamped backup directory
#   IF creation fails THEN exit with error
################################################################################
create_backup_directory() {
    log_message "INFO" "Creating backup directory: ${BACKUP_DIR}"
    
    # PSEUDO CODE: Create directory with full path
    mkdir -p "${BACKUP_DIR}" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        log_message "ERROR" "Failed to create backup directory"
        return 1
    fi
    
    log_message "INFO" "Backup directory created successfully"
    return 0
}

################################################################################
# FUNCTION: backup_home_assistant
# PSEUDO CODE:
#   COPY all Home Assistant config files to backup directory
#   EXCLUDE database files (too large, not critical for config backup)
#   LOG success or failure
################################################################################
backup_home_assistant() {
    log_message "INFO" "Backing up Home Assistant configuration..."
    
    # PSEUDO CODE: Check if source exists
    if [ ! -d "${HOME_ASSISTANT_DIR}" ]; then
        log_message "WARN" "Home Assistant directory not found: ${HOME_ASSISTANT_DIR}"
        return 1
    fi
    
    # PSEUDO CODE: Copy files, excluding large/unnecessary items
    # COMMON LANGUAGE: Copy config files but skip database and logs
    rsync -a \
        --exclude='home-assistant.log*' \
        --exclude='*.db' \
        --exclude='*.db-shm' \
        --exclude='*.db-wal' \
        --exclude='deps/' \
        --exclude='tts/' \
        --exclude='.storage/' \
        "${HOME_ASSISTANT_DIR}/" \
        "${BACKUP_DIR}/home-assistant/" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "Home Assistant backup completed"
        return 0
    else
        log_message "ERROR" "Home Assistant backup failed"
        return 1
    fi
}

################################################################################
# FUNCTION: backup_esphome
# PSEUDO CODE:
#   COPY all ESPHome YAML configurations to backup
#   INCLUDE common files
#   EXCLUDE compiled firmware binaries (can be rebuilt)
################################################################################
backup_esphome() {
    log_message "INFO" "Backing up ESPHome configurations..."
    
    if [ ! -d "${ESPHOME_DIR}" ]; then
        log_message "WARN" "ESPHome directory not found: ${ESPHOME_DIR}"
        return 1
    fi
    
    # PSEUDO CODE: Copy YAML files only, skip compiled binaries
    rsync -a \
        --include='*.yaml' \
        --include='*.yml' \
        --include='common/' \
        --exclude='.esphome/' \
        --exclude='*.bin' \
        "${ESPHOME_DIR}/" \
        "${BACKUP_DIR}/esphome/" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "ESPHome backup completed"
        return 0
    else
        log_message "ERROR" "ESPHome backup failed"
        return 1
    fi
}

################################################################################
# FUNCTION: backup_mqtt
# PSEUDO CODE:
#   COPY MQTT broker configuration
#   EXCLUDE data and log files (only config needed for restore)
################################################################################
backup_mqtt() {
    log_message "INFO" "Backing up MQTT configuration..."
    
    if [ ! -d "${MQTT_DIR}" ]; then
        log_message "WARN" "MQTT directory not found: ${MQTT_DIR}"
        return 1
    fi
    
    # PSEUDO CODE: Copy only config files
    mkdir -p "${BACKUP_DIR}/mqtt/config"
    
    if [ -f "${MQTT_DIR}/config/mosquitto.conf" ]; then
        cp "${MQTT_DIR}/config/mosquitto.conf" "${BACKUP_DIR}/mqtt/config/" 2>/dev/null
    fi
    
    if [ -f "${MQTT_DIR}/config/passwd" ]; then
        cp "${MQTT_DIR}/config/passwd" "${BACKUP_DIR}/mqtt/config/" 2>/dev/null
    fi
    
    log_message "INFO" "MQTT backup completed"
    return 0
}

################################################################################
# FUNCTION: backup_scripts
# PSEUDO CODE:
#   COPY all utility scripts to backup
#   PRESERVE executable permissions
################################################################################
backup_scripts() {
    log_message "INFO" "Backing up utility scripts..."
    
    if [ ! -d "${SCRIPTS_DIR}" ]; then
        log_message "WARN" "Scripts directory not found: ${SCRIPTS_DIR}"
        return 1
    fi
    
    rsync -a "${SCRIPTS_DIR}/" "${BACKUP_DIR}/scripts/" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "Scripts backup completed"
        return 0
    else
        log_message "ERROR" "Scripts backup failed"
        return 1
    fi
}

################################################################################
# FUNCTION: create_backup_manifest
# PSEUDO CODE:
#   CREATE text file listing backup contents
#   INCLUDE timestamps, file counts, sizes
#   COMMON LANGUAGE: Like a receipt showing what's in the backup
################################################################################
create_backup_manifest() {
    log_message "INFO" "Creating backup manifest..."
    
    local manifest_file="${BACKUP_DIR}/MANIFEST.txt"
    
    # PSEUDO CODE: Write backup metadata
    {
        echo "Garden Automation System Backup"
        echo "================================"
        echo "Backup Date: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Backup Name: ${BACKUP_NAME}"
        echo ""
        echo "Contents:"
        echo "--------"
        find "${BACKUP_DIR}" -type f | sed "s|${BACKUP_DIR}/||" | sort
        echo ""
        echo "Statistics:"
        echo "-----------"
        echo "Total Files: $(find "${BACKUP_DIR}" -type f | wc -l)"
        echo "Total Size: $(du -sh "${BACKUP_DIR}" | cut -f1)"
    } > "${manifest_file}"
    
    log_message "INFO" "Backup manifest created"
}

################################################################################
# FUNCTION: compress_backup
# PSEUDO CODE:
#   COMPRESS backup directory into .tar.gz archive
#   DELETE uncompressed directory after successful compression
#   COMMON LANGUAGE: Zip up all the files into one compressed archive
################################################################################
compress_backup() {
    log_message "INFO" "Compressing backup..."
    
    local archive_name="${BACKUP_ROOT}/${BACKUP_NAME}.tar.gz"
    
    # PSEUDO CODE: Create compressed archive
    # -c: create archive
    # -z: compress with gzip
    # -f: filename
    # -C: change directory (for clean paths in archive)
    tar -czf "${archive_name}" -C "${BACKUP_ROOT}" "${BACKUP_NAME}" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        local archive_size=$(du -h "${archive_name}" | cut -f1)
        log_message "INFO" "Backup compressed successfully (${archive_size})"
        
        # PSEUDO CODE: Remove uncompressed directory to save space
        rm -rf "${BACKUP_DIR}"
        log_message "INFO" "Temporary backup directory removed"
        return 0
    else
        log_message "ERROR" "Backup compression failed"
        return 1
    fi
}

################################################################################
# FUNCTION: cleanup_old_backups
# PSEUDO CODE:
#   FIND backups older than RETENTION_DAYS
#   DELETE old backups to free disk space
#   LOG deletion count
################################################################################
cleanup_old_backups() {
    log_message "INFO" "Cleaning up old backups (keeping last ${RETENTION_DAYS} days)..."
    
    # PSEUDO CODE: Find and delete old backup files
    local deleted_count=0
    
    # Find .tar.gz files older than retention period
    while IFS= read -r old_backup; do
        log_message "INFO" "Deleting old backup: $(basename "$old_backup")"
        rm -f "$old_backup"
        ((deleted_count++))
    done < <(find "${BACKUP_ROOT}" -name "garden_automation_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS})
    
    if [ $deleted_count -gt 0 ]; then
        log_message "INFO" "Deleted ${deleted_count} old backup(s)"
    else
        log_message "INFO" "No old backups to delete"
    fi
}

################################################################################
# FUNCTION: verify_backup
# PSEUDO CODE:
#   TEST integrity of compressed backup
#   ENSURE archive can be extracted
#   COMMON LANGUAGE: Make sure the backup isn't corrupted
################################################################################
verify_backup() {
    log_message "INFO" "Verifying backup integrity..."
    
    local archive_name="${BACKUP_ROOT}/${BACKUP_NAME}.tar.gz"
    
    # PSEUDO CODE: Test archive without extracting
    tar -tzf "${archive_name}" >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        log_message "INFO" "Backup verification successful"
        return 0
    else
        log_message "ERROR" "Backup verification failed - archive may be corrupted"
        return 1
    fi
}

################################################################################
# MAIN EXECUTION FLOW
################################################################################

log_message "INFO" "=========================================="
log_message "INFO" "Garden Automation Backup Script Starting"
log_message "INFO" "=========================================="

# STEP 1: Check prerequisites
if ! check_prerequisites; then
    log_message "ERROR" "Prerequisites check failed. Exiting."
    exit 1
fi

# STEP 2: Create backup directory
if ! create_backup_directory; then
    log_message "ERROR" "Failed to create backup directory. Exiting."
    exit 1
fi

# STEP 3: Backup all components
backup_home_assistant
backup_esphome
backup_mqtt
backup_scripts

# STEP 4: Create manifest
create_backup_manifest

# STEP 5: Compress backup
if ! compress_backup; then
    log_message "ERROR" "Backup compression failed. Exiting."
    exit 1
fi

# STEP 6: Verify backup integrity
if ! verify_backup; then
    log_message "WARN" "Backup verification failed but backup was created"
fi

# STEP 7: Cleanup old backups
cleanup_old_backups

# STEP 8: Final summary
log_message "INFO" "=========================================="
log_message "INFO" "Backup completed successfully!"
log_message "INFO" "Backup location: ${BACKUP_ROOT}/${BACKUP_NAME}.tar.gz"
log_message "INFO" "=========================================="

exit 0

################################################################################
# RESTORE PROCEDURE (MANUAL)
################################################################################
#
# TO RESTORE FROM BACKUP:
#
# 1. Stop all containers:
#    docker-compose down
#
# 2. Extract backup:
#    tar -xzf /backups/garden_automation_backup_TIMESTAMP.tar.gz -C /tmp
#
# 3. Restore Home Assistant:
#    rsync -a /tmp/garden_automation_backup_TIMESTAMP/home-assistant/ ./home-assistant/
#
# 4. Restore ESPHome:
#    rsync -a /tmp/garden_automation_backup_TIMESTAMP/esphome/ ./esphome/
#
# 5. Restore MQTT:
#    rsync -a /tmp/garden_automation_backup_TIMESTAMP/mqtt/ ./mqtt/
#
# 6. Restart containers:
#    docker-compose up -d
#
# 7. Verify services:
#    docker-compose logs -f
#
################################################################################

