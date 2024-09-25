import subprocess
import os
import sys
import ctypes
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

# Set up logging
LOG_FILENAME = 'system_health_check.log'
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configure rotating log handler (5 MB max per file, 3 backups)
log_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=5*1024*1024, backupCount=3)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

# Set up logging to both file and console
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# Check if running as Admin
def is_admin():
    try:
        is_admin_status = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin_status:
            logger.info("Script is running with administrative privileges.")
        else:
            logger.error("Script is not running as Administrator. Please run as Administrator.")
        return is_admin_status
    except Exception as e:
        logger.error(f"Error checking administrative privileges: {str(e)}")
        return False

# Run a command in the command prompt and capture the output
def run_command(command):
    logger.info(f"Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            logger.info(f"Command executed successfully: {command}")
            return result.stdout.strip(), None
        else:
            logger.error(f"Command failed with return code {result.returncode}: {command}")
            return None, result.stderr.strip()
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {command}")
        return None, "Timeout"
    except Exception as e:
        logger.error(f"Error executing command: {command} - {str(e)}")
        return None, str(e)

# Check Disk Health using CHKDSK
def check_disk_health():
    logger.info("\nChecking Disk Health (CHKDSK)...")
    chkdsk_cmd = "chkdsk C: /scan"
    output, error = run_command(chkdsk_cmd)
    if error:
        logger.error(f"Error running CHKDSK: {error}")
    else:
        logger.info(output)

# System File Checker (SFC)
def run_sfc_scan():
    logger.info("\nRunning System File Checker (SFC)...")
    sfc_cmd = "sfc /scannow"
    output, error = run_command(sfc_cmd)
    if error:
        logger.error(f"Error running SFC: {error}")
    else:
        logger.info(output)

# Deployment Imaging Service and Management Tool (DISM)
def run_dism_scan():
    logger.info("\nRunning Deployment Imaging Service and Management Tool (DISM)...")
    dism_cmd = "dism /online /cleanup-image /scanhealth"
    output, error = run_command(dism_cmd)
    if error:
        logger.error(f"Error running DISM: {error}")
    else:
        logger.info(output)

# DISM Repair if issues are detected
def run_dism_repair():
    logger.info("\nAttempting to repair Windows image using DISM...")
    dism_cmd = "dism /online /cleanup-image /restorehealth"
    output, error = run_command(dism_cmd)
    if error:
        logger.error(f"Error running DISM repair: {error}")
    else:
        logger.info(output)

# Check Windows Event Logs for Critical Errors
def check_event_logs():
    logger.info("\nChecking Event Logs for critical errors...")
    event_log_cmd = 'wevtutil qe System /f:text /c:10 /rd:true /q:"*[System[(Level=1 or Level=2 or Level=3)]]"'
    output, error = run_command(event_log_cmd)
    if error:
        logger.error(f"Error retrieving event logs: {error}")
    else:
        logger.info(output)

# Main function to run health checks
def run_health_check():
    if not is_admin():
        logger.critical("This script requires administrative privileges. Please run the script as an administrator.")
        sys.exit(1)

    logger.info(f"System Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("==============================================")

    # Define all the health checks to be run
    health_checks = [run_sfc_scan, run_dism_scan, run_dism_repair, check_disk_health, check_event_logs]

    # Use ThreadPoolExecutor to run the checks in parallel
    num_cores = multiprocessing.cpu_count()
    logger.info(f"Utilizing all {num_cores} cores for parallel health checks.")

    # Execute health checks in parallel
    with ThreadPoolExecutor(max_workers=num_cores) as executor:
        future_checks = {executor.submit(check): check.__name__ for check in health_checks}
        for future in as_completed(future_checks):
            check_name = future_checks[future]
            try:
                future.result()  # Get the result to handle any exceptions
            except Exception as e:
                logger.error(f"{check_name} raised an exception: {str(e)}")

    logger.info("\nSystem health check completed!")


if __name__ == "__main__":
    try:
        run_health_check()
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")