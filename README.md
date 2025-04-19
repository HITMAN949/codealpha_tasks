# System Maintenance & Automation Script

This Python script automates several system maintenance and data processing tasks, including:

- **Log Processing**: Extracts errors and warnings from log files.
- **Data Cleaning**: Cleans raw CSV files by removing duplicates, filling missing values, and standardizing date formats.
- **System Monitoring**: Monitors disk space, CPU, and memory usage.
- **Log Rotation**: Archives large log files and resets them.
- **Email Alerts**: Sends email notifications when disk usage, CPU, or memory usage exceeds specified thresholds.

This project is a part of the **Code Alpha Python Programming Internship**.

## Features

1. **Process Log Files**  
   - Extracts lines containing errors or warnings from log files and saves them to a new file.
   
2. **Clean Data**  
   - Cleans raw CSV files by removing duplicates, filling missing values, and standardizing date formats.
   
3. **Check Disk Space**  
   - Monitors disk usage and sends an email alert if usage exceeds a specified threshold (default: 80%).

4. **Check System Resources (CPU & Memory)**  
   - Monitors CPU and memory usage and sends an email alert if usage exceeds specified thresholds (default: 80%).

5. **Rotate Logs**  
   - Archives log files that exceed a specified size and creates a new, empty log file.

6. **Email Alerts**  
   - Sends email notifications when critical thresholds are exceeded (e.g., disk space, CPU, or memory usage).

## Installation

### Prerequisites

1. Python 3.9  
2. Install required Python packages using `pip`:

```bash
pip install -r requirements.txt
```
3. Run the script:
```bash
python system_maintenance_automation.py
```
4. Select an option from the menu to execute a task:
```bash
--- System Maintenance & Automation Menu ---
1. Process log files
2. Clean data
3. Check disk space
4. Check system resources (CPU & Memory)
5. Rotate logs
6. Exit
```
