import pyautogui as pag
import random
import time
import threading
import datetime
import logging
import smtplib
from email.message import EmailMessage
#import os
import json

# Load configuration from JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Configuration
MOVE_INTERVAL = 120                                             # seconds between mouse movements
AFK_THRESHOLD = 60                                              # how many seconds before considered AFK
FRIDAY_START = (16, 30)                                         # 4:10 PM
FRIDAY_END = (18, 30)                                           # 6:30 PM
CUSTOM_MODE = config["CUSTOM_MODE"]
CUSTOM_START_HOUR = config["CUSTOM_START_HOUR"]
CUSTOM_START_MIN = config["CUSTOM_START_MIN"]
CUSTOM_DURATION_HOURS = config["CUSTOM_DURATION_HOURS"]
EMAIL_SENDER = config["EMAIL_SENDER"]
EMAIL_RECEIVER = config["EMAIL_RECEIVER"]                       # or a different receiver
EMAIL_SUBJECT = config["EMAIL_SUBJECT"]
APP_PASSWORD = config["APP_PASSWORD"]                           # use Gmail App Password, not your regular password

# Determine an alternating log file based on week number
week_number = datetime.date.today().isocalendar().week
log_file = "afk_log1.log" if week_number % 2 else "afk_log2.log"

# Setup logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s —— %(message)s')

def is_friday_window():
    now = datetime.datetime.now()
    start = now.replace(hour=FRIDAY_START[0], minute=FRIDAY_START[1], second=0, microsecond=0)
    end = now.replace(hour=FRIDAY_END[0], minute=FRIDAY_END[1], second=0, microsecond=0)
    return now.weekday() == 4 and start <= now <= end

# Manual duration setting function — for example, runs for 2 hours excluding 5–7 PM
def is_within_custom_window(start_hour, start_min, duration_hours):
    now = datetime.datetime.now()
    custom_start = now.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
    custom_end = custom_start + datetime.timedelta(hours=duration_hours)

    block_start = now.replace(hour=17, minute=0, second=0, microsecond=0)
    block_end = now.replace(hour=19, minute=0, second=0, microsecond=0)

    if custom_start <= now <= custom_end:
        if now < block_start or now >= block_end:
            return True
    return False

def move_mouse_randomly():
    screen_width, screen_height = pag.size()
    x = random.randint(0, screen_width - 1)
    y = random.randint(0, screen_height - 1)
    pag.moveTo(x, y, duration=0.5)
    logging.info(f"Mouse moved to ({x}, {y})")

def send_log_email():
    try:
        with open(log_file, 'r') as file:
            content = file.read()

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = EMAIL_SUBJECT + f" — Week {week_number}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, APP_PASSWORD)
            smtp.send_message(msg)

        print("Log email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def afk_monitor():
    curr_coords = pag.position()
    afk_counter = 0
    try:
        while True:
            if CUSTOM_MODE:
                active = is_within_custom_window(CUSTOM_START_HOUR, CUSTOM_START_MIN, CUSTOM_DURATION_HOURS)
            else:
                active = is_friday_window()

            if active:
                if pag.position() == curr_coords:
                    afk_counter += 1
                else:
                    afk_counter = 0
                    curr_coords = pag.position()

                if afk_counter > AFK_THRESHOLD:
                    move_mouse_randomly()
                    curr_coords = pag.position()
                    afk_counter = 0

                logging.info(f"AFK Counter: {afk_counter}")
            else:
                logging.info("Outside active window. Sleeping...")
                time.sleep(120)                                   # sleep longer if not in active time

            time.sleep(1)
    except KeyboardInterrupt:
        print("Bot interrupted manually.")
    finally:
        send_log_email()
        with open(log_file, 'w') as f:
            f.write("")
        print("Log cleared.")

if __name__ == "__main__":
    print(f"AFK bot started — using log file: {log_file}")
    print("Runs only on Fridays 4:00–6:30 PM unless custom mode is enabled.")
    monitor_thread = threading.Thread(target=afk_monitor)
    monitor_thread.start()
