# IP_Watcher.py

**Written by:** John G. Asmussen  
**Organization:** EGA Technology Specialists, LLC.  
**License:** GNU GPL v3.0

---

## Overview

IP_Watcher.py monitors your machine's public IP address and sends an email notification via Gmail whenever it changes. It is designed to run automatically and unattended as a cron job.

---

## Requirements

### System Requirements

- Python 3.6 or higher
- A Gmail account with **2-Factor Authentication (2FA)** enabled
- A Gmail **App Password** (required — regular Gmail passwords will not work)

### Python Dependencies

**Note:** `smtplib`, `urllib`, `re`, `os`, `ssl`, and `email` are all part of the Python standard library and require no separate installation.

---

## Initial Setup

### Step 1 — Enable 2FA on Your Google Account

Gmail requires 2FA to be active before you can generate an App Password.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Under **"How you sign in to Google"**, enable **2-Step Verification** if it is not already active

---

### Step 2 — Generate a Gmail App Password

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in if prompted
3. Enter a name for the app password (e.g. `IP Watcher`)
4. Click **Create**
5. Copy the 16-character password that is displayed — **you will not be able to see it again**

---

### Step 3 — Create the Log File

The script reads and writes to `/var/log/IP_Watcher.log`. Create the file and assign ownership to the user that will run the script (replace `ubuntu` with your username if different):

```bash
sudo touch /var/log/IP_Watcher.log
sudo chown ubuntu:ubuntu /var/log/IP_Watcher.log
sudo chmod 644 /var/log/IP_Watcher.log
```

Verify the permissions look correct:

```bash
ls -l /var/log/IP_Watcher.log
```

Expected output:

```
-rw-r--r-- 1 ubuntu ubuntu 0 Jan 01 00:00 /var/log/IP_Watcher.log
```

---

### Step 4 — Place the Script

Copy `IP_Watcher.py` to your home directory (or any location of your choice):

```bash
cp IP_Watcher.py /home/ubuntu/IP_Watcher.py
chmod +x /home/ubuntu/IP_Watcher.py
```

---

## Setting Up the Cron Job

Cron does **not** read your `.bashrc` or `.bash_profile`, so environment variables must be defined directly inside the crontab. This is the recommended approach for this script.

### Step 5 — Open the Crontab Editor

```bash
crontab -e
```

If this is your first time, you will be asked to choose a text editor. `nano` is the easiest option for most users.

---

### Step 6 — Add the Environment Variables and Cron Entry

Paste the following block at the **top** of your crontab file, filling in your actual values:

```
IPWATCHER_MACHINE_NAME="My Home Server"
IPWATCHER_FROM_EMAIL="sender@gmail.com"
IPWATCHER_TO_EMAILS="recipient@example.com"
IPWATCHER_SMTP_USER="sender@gmail.com"
IPWATCHER_SMTP_PASS="abcd efgh ijkl mnop"
```

Then add the cron schedule entry below the variables. The example below runs the script **every 15 minutes**:

```
*/15 * * * * /usr/bin/python3 /home/ubuntu/IP_Watcher.py
```

Your complete crontab should look like this when done:

```
IPWATCHER_MACHINE_NAME="My Home Server"
IPWATCHER_FROM_EMAIL="sender@gmail.com"
IPWATCHER_TO_EMAILS="recipient@example.com"
IPWATCHER_SMTP_USER="sender@gmail.com"
IPWATCHER_SMTP_PASS="abcd efgh ijkl mnop"

*/15 * * * * /usr/bin/python3 /home/ubuntu/IP_Watcher.py
```

Save and exit the editor (`Ctrl+O`, then `Ctrl+X` in nano).

---

### Step 7 — Verify the Cron Job Was Saved

```bash
crontab -l
```

You should see your variables and the schedule entry listed.

---

### Step 8 — Test the Script Manually

Before waiting for cron to fire, run the script manually to confirm everything is working:

```bash
IPWATCHER_MACHINE_NAME="My Home Server" \
IPWATCHER_FROM_EMAIL="sender@gmail.com" \
IPWATCHER_TO_EMAILS="recipient@example.com" \
IPWATCHER_SMTP_USER="sender@gmail.com" \
IPWATCHER_SMTP_PASS="abcd efgh ijkl mnop" \
/usr/bin/python3 /home/ubuntu/IP_Watcher.py
```

If the IP has changed since the last run (or the log file is empty), you should receive an email notification. If the IP is unchanged, you will see:

```
IP unchanged: 123.456.789.000
```

---

## Cron Schedule Reference

Adjust the schedule to suit your needs:

| Schedule | Cron Expression |
|---|---|
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every 30 minutes | `*/30 * * * *` |
| Every hour | `0 * * * *` |
| Once a day at midnight | `0 0 * * *` |

---

## Sending to Multiple Recipients

To notify more than one email address, separate addresses with commas in the `IPWATCHER_TO_EMAILS` variable:

```
IPWATCHER_TO_EMAILS="person1@example.com,person2@example.com"
```

---

## Troubleshooting

**`SMTPAuthenticationError (535)`** — Gmail rejected the login. Make sure you are using an App Password and not your regular Gmail password. Regenerate the App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) if needed.

**Script runs manually but not via cron** — Confirm the environment variables are defined at the top of the crontab file and that the path to Python is correct. Verify with `which python3`.

**Permission denied on log file** — Re-run the `chown` and `chmod` commands in Step 3, making sure the username matches the user whose crontab you edited.

**No email received but no error** — Check that the IP address actually changed since the last run. Temporarily delete the contents of `/var/log/IP_Watcher.log` to force a notification on the next run:

```bash
echo "" > /var/log/IP_Watcher.log
```

---

## Security Notes

- Your App Password is stored in the crontab. Access to the crontab is restricted to your user and root by default.
- For environments with stricter security requirements, consider storing credentials in a dedicated file with permissions set to `600` (owner read/write only) and sourcing it from the crontab.
- Never commit your App Password or any credentials to version control.
