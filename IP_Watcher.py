#!/usr/bin/env python3
######################################################
#                   IP_Watcher.py                    #
#----------------------------------------------------#
#           Written by: John G. Asmussen             #
#         EGA Technology Specialists, LLC.           #
#                   GNU GPL v3.0                     #
######################################################

import os
import re
import smtplib
import ssl
import urllib.request
import urllib.error
from email.mime.text import MIMEText

# --- Configuration (load sensitive values from environment variables) ---
LOG_FILE      = '/var/log/IP_Watcher.log'
MACHINE_NAME  = os.environ.get('IPWATCHER_MACHINE_NAME', '')
FROM_ADDR     = os.environ.get('IPWATCHER_FROM_EMAIL', '')
TO_ADDRS      = os.environ.get('IPWATCHER_TO_EMAILS', '').split(',')  # comma-separated
SMTP_USER     = os.environ.get('IPWATCHER_SMTP_USER', '')
SMTP_PASS     = os.environ.get('IPWATCHER_SMTP_PASS', '')
SMTP_HOST     = 'smtp.gmail.com'
SMTP_PORT     = 587
IP_URL        = 'https://checkip.amazonaws.com'
IP_REGEX      = re.compile(r'\b(\d{1,3}\.){3}\d{1,3}\b')
REQUEST_TIMEOUT = 10  # seconds

def fetch_current_ip() -> str:
    """Fetch the current public IP from a remote service."""
    try:
        with urllib.request.urlopen(IP_URL, timeout=REQUEST_TIMEOUT) as response:
            content = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to fetch IP address: {e}") from e

    match = IP_REGEX.search(content)
    if not match:
        raise ValueError(f"No valid IP address found in response: {content!r}")
    return match.group(0)

def read_previous_ip() -> str:
    """Read the last known IP from the log file."""
    try:
        with open(LOG_FILE, 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        return ''
    except OSError as e:
        raise RuntimeError(f"Could not read log file: {e}") from e

def write_current_ip(ip: str) -> None:
    """Persist the current IP to the log file."""
    try:
        with open(LOG_FILE, 'w') as f:
            f.write(ip)
    except OSError as e:
        raise RuntimeError(f"Could not write log file: {e}") from e

def send_notification(new_ip: str) -> None:
    """Send an email notification about the IP change."""
    subject = f"IP Address Change Detected: {MACHINE_NAME}"
    body    = f"The new public IP address of {MACHINE_NAME} is: {new_ip}"

    context = ssl.create_default_context()  # enforces certificate verification

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=REQUEST_TIMEOUT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)

            for recipient in TO_ADDRS:
                recipient = recipient.strip()
                if not recipient:
                    continue
                msg            = MIMEText(body)
                msg['Subject'] = subject
                msg['From']    = FROM_ADDR
                msg['To']      = recipient
                server.sendmail(FROM_ADDR, recipient, msg.as_string())
                print(f"Notification sent to {recipient}")
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}") from e

def main() -> None:
    current_ip  = fetch_current_ip()
    previous_ip = read_previous_ip()

    if current_ip != previous_ip:
        print(f"IP changed: {previous_ip!r} -> {current_ip!r}")
        send_notification(current_ip)
        write_current_ip(current_ip)
    else:
        print(f"IP unchanged: {current_ip}")

if __name__ == '__main__':
    main()
