#!/usr/bin/env python3
"""
ISS Overhead Notifier
Tracks the International Space Station and sends email notifications 
when it's overhead during nighttime.

Author: Hamed Ahmadbeigi
Date: 2025
"""

import requests
import smtplib
import time
import logging
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import configuration
try:
    from config import MY_LAT, MY_LONG, MY_EMAIL, MY_PASSWORD, TO_EMAIL
except ImportError:
    print("⚠️  Error: config.py not found!")
    print("Please copy config.example.py to config.py and update your settings.")
    exit(1)

# Constants
ISS_API_URL = "http://api.open-notify.org/iss-now.json"
SUNRISE_API_URL = "https://api.sunrise-sunset.org/json"
CHECK_INTERVAL = 60  # seconds
POSITION_TOLERANCE = 5  # degrees

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iss_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ISSTracker:
    """ISS Overhead Notifier Class"""
    
    def __init__(self):
        self.last_notification = None
        self.notification_cooldown = 3600  # 1 hour between notifications
        logger.info("🛰️  ISS Tracker initialized")
        logger.info(f"📍 Monitoring location: {MY_LAT:.3f}, {MY_LONG:.3f}")
    
    def get_iss_position(self):
        """Fetch current ISS position from API"""
        try:
            response = requests.get(ISS_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            iss_lat = float(data["iss_position"]["latitude"])
            iss_long = float(data["iss_position"]["longitude"])
            
            logger.debug(f"ISS Position: {iss_lat:.3f}, {iss_long:.3f}")
            return iss_lat, iss_long
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch ISS position: {e}")
            return None, None
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid ISS API response: {e}")
            return None, None
    
    def is_iss_overhead(self):
        """Check if ISS is overhead (within tolerance range)"""
        iss_lat, iss_long = self.get_iss_position()
        
        if iss_lat is None or iss_long is None:
            return False
        
        lat_match = (MY_LAT - POSITION_TOLERANCE <= iss_lat <= MY_LAT + POSITION_TOLERANCE)
        long_match = (MY_LONG - POSITION_TOLERANCE <= iss_long <= MY_LONG + POSITION_TOLERANCE)
        
        is_overhead = lat_match and long_match
        
        if is_overhead:
            logger.info(f"🎯 ISS is overhead! Position: {iss_lat:.3f}, {iss_long:.3f}")
        else:
            logger.debug(f"ISS not overhead. Position: {iss_lat:.3f}, {iss_long:.3f}")
            
        return is_overhead
    
    def get_sun_times(self):
        """Get sunrise and sunset times for current location"""
        try:
            params = {
                "lat": MY_LAT,
                "lng": MY_LONG,
                "formatted": 0,
            }
            
            response = requests.get(SUNRISE_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Parse UTC times and convert to local hour
            sunrise_utc = data["results"]["sunrise"]
            sunset_utc = data["results"]["sunset"]
            
            # Extract hour from ISO format (simplified)
            sunrise_hour = int(sunrise_utc.split("T")[1].split(":")[0])
            sunset_hour = int(sunset_utc.split("T")[1].split(":")[0])
            
            logger.debug(f"Sunrise: {sunrise_hour}:00 UTC, Sunset: {sunset_hour}:00 UTC")
            return sunrise_hour, sunset_hour
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch sun times: {e}")
            return None, None
        except (KeyError, ValueError) as e:
            logger.error(f"Invalid sunrise/sunset API response: {e}")
            return None, None
    
    def is_nighttime(self):
        """Check if it's currently nighttime"""
        sunrise_hour, sunset_hour = self.get_sun_times()
        
        if sunrise_hour is None or sunset_hour is None:
            logger.warning("⚠️  Could not determine sun times, assuming daytime")
            return False
        
        current_hour = datetime.now(timezone.utc).hour
        
        # Check if current time is after sunset or before sunrise
        is_night = current_hour >= sunset_hour or current_hour <= sunrise_hour
        
        logger.debug(f"Current hour: {current_hour} UTC, Night: {is_night}")
        return is_night
    
    def should_send_notification(self):
        """Check if enough time has passed since last notification"""
        if self.last_notification is None:
            return True
        
        time_since_last = time.time() - self.last_notification
        return time_since_last > self.notification_cooldown
    
    def send_email_notification(self):
        """Send email notification about ISS overhead"""
        if not self.should_send_notification():
            logger.info("⏰ Skipping notification (cooldown active)")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = MY_EMAIL
            msg['To'] = TO_EMAIL
            msg['Subject'] = "🛰️ ISS is Overhead!"
            
            # Email body
            body = f"""
Hello Space Enthusiast! 🌌

The International Space Station (ISS) is currently passing overhead at your location!

📍 Your Location: {MY_LAT:.3f}, {MY_LONG:.3f}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌙 Conditions: Nighttime (perfect for viewing!)

Step outside and look up! The ISS appears as a bright, fast-moving star across the sky.

Fun facts:
• The ISS orbits Earth every ~90 minutes
• It travels at about 17,500 mph
• It's about the size of a football field
• It's the third brightest object in the sky after the Sun and Moon

Happy stargazing! ⭐

---
Sent by ISS Overhead Notifier
            """.strip()
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(MY_EMAIL, MY_PASSWORD)
                server.send_message(msg)
            
            self.last_notification = time.time()
            logger.info(f"📧 Email notification sent to {TO_EMAIL}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ Email authentication failed. Check your email/password settings.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error sending email: {e}")
            return False
    
    def run(self):
        """Main tracking loop"""
        logger.info("🚀 Starting ISS tracking...")
        logger.info(f"⏱️  Checking every {CHECK_INTERVAL} seconds")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                logger.debug("🔍 Checking ISS position...")
                
                # Check conditions
                iss_overhead = self.is_iss_overhead()
                is_night = self.is_nighttime()
                
                if iss_overhead and is_night:
                    logger.info("🎉 ISS is overhead during nighttime!")
                    success = self.send_email_notification()
                    if success:
                        logger.info("✅ Notification sent successfully")
                    else:
                        logger.warning("⚠️  Failed to send notification")
                elif iss_overhead:
                    logger.info("☀️  ISS is overhead but it's daytime")
                elif is_night:
                    logger.debug("🌙 It's nighttime but ISS is not overhead")
                else:
                    logger.debug("☀️  Daytime and ISS not overhead")
                
                # Wait before next check
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("\n👋 ISS Tracker stopped by user")
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")
            raise

def test_email_settings():
    """Test email configuration"""
    print("🧪 Testing email settings...")
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(MY_EMAIL, MY_PASSWORD)
            print("✅ Email authentication successful!")
            return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Email authentication failed.")
        print("Make sure you're using a Gmail App Password, not your regular password.")
        return False
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

def main():
    """Main function"""
    print("🛰️  ISS Overhead Notifier")
    print("=" * 50)
    
    # Test email settings first
    if not test_email_settings():
        print("\n⚠️  Please fix email settings before running the tracker.")
        return
    
    # Start tracking
    tracker = ISSTracker()
    tracker.run()

if __name__ == "__main__":
    main()
