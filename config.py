"""
Configuration file for ISS Overhead Notifier

Instructions:
1. Copy this file to 'config.py'
2. Update the values below with your information
3. Never commit config.py to version control (it's in .gitignore)
"""

# Your coordinates (latitude, longitude)
# Get these from Google Maps by right-clicking on your location
MY_LAT = 51.507351    # Example: London, UK
MY_LONG = -0.127758   # Example: London, UK

# Email settings (Gmail only)
# IMPORTANT: Use Gmail App Password, not your regular password
# Instructions: https://support.google.com/accounts/answer/185833
MY_EMAIL = "your.email@gmail.com"
MY_PASSWORD = "your-gmail-app-password"  # 16-character app password

# Notification recipient (can be same as MY_EMAIL)
TO_EMAIL = "recipient@gmail.com"

# Optional: Customize these settings
CHECK_INTERVAL = 60  # How often to check (seconds)
POSITION_TOLERANCE = 5  # How close ISS needs to be (degrees)
