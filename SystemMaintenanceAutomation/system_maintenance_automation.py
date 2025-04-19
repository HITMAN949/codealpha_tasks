import os
import pandas as pd
import re
from datetime import datetime
import shutil
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def process_log_files(log_directory, error_keywords=["ERROR", "WARNING"]):
    error_logs = []
    for log_file in os.listdir(log_directory):
        log_path = os.path.join(log_directory, log_file)
        if os.path.isdir(log_path):
            continue
        with open(log_path, 'r') as file:
            logs = file.readlines()
            for line in logs:
                if any(keyword in line for keyword in error_keywords):
                    error_logs.append(line)
    error_log_file = os.path.join(log_directory, "error_log_report.txt")
    with open(error_log_file, 'w') as report:
        for error in error_logs:
            report.write(error)
    print(f"Log processing completed. Errors saved to {error_log_file}")

def clean_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df.drop_duplicates(inplace=True)
    df.fillna(df.mean(), inplace=True)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df.to_csv(output_file, index=False)
    print(f"Data cleaning completed. Cleaned data saved to {output_file}")

def check_disk_space(threshold=80):
    disk_usage = psutil.disk_usage('/')
    usage_percent = disk_usage.percent
    print(f"Disk Usage: {usage_percent}%")
    if usage_percent > threshold:
        print(f"Warning: Disk usage is above {threshold}%!")
        send_email_alert(f"Disk Usage Alert: {usage_percent}% used")
    return usage_percent

def check_system_resources(cpu_threshold=80, memory_threshold=80):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    if cpu_usage > cpu_threshold:
        print(f"Warning: CPU usage is above {cpu_threshold}%!")
        send_email_alert(f"CPU Usage Alert: {cpu_usage}% used")
    if memory_usage > memory_threshold:
        print(f"Warning: Memory usage is above {memory_threshold}%!")
        send_email_alert(f"Memory Usage Alert: {memory_usage}% used")

def rotate_logs(log_directory, max_log_size=1000000):
    for log_file in os.listdir(log_directory):
        log_path = os.path.join(log_directory, log_file)
        if os.path.getsize(log_path) > max_log_size:
            archived_file = f"{log_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            shutil.move(log_path, archived_file)
            print(f"Archived {log_file} due to size limit. New file created.")
            with open(log_path, 'w') as new_file:
                new_file.write("")

def send_email_alert(message, to_email="recipient@example.com", from_email="sender@example.com"):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, "your_password")
        subject = "System Alert"
        body = message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")

def main_menu():
    while True:
        print("\n--- System Maintenance & Automation Menu ---")
        print("1. Process log files")
        print("2. Clean data")
        print("3. Check disk space")
        print("4. Check system resources (CPU & Memory)")
        print("5. Rotate logs")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")

        if choice == "1":
            log_directory = input("Enter log directory path: ")
            process_log_files(log_directory)
        elif choice == "2":
            data_file = input("Enter data file path: ")
            cleaned_data_file = input("Enter path to save cleaned data: ")
            clean_data(data_file, cleaned_data_file)
        elif choice == "3":
            check_disk_space()
        elif choice == "4":
            check_system_resources()
        elif choice == "5":
            log_directory = input("Enter log directory path: ")
            rotate_logs(log_directory)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
