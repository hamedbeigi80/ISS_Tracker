# 🛰️ ISS Overhead Notifier

Get email notifications when the International Space Station (ISS) is passing overhead during nighttime! Perfect for stargazers and space enthusiasts who want to catch a glimpse of the ISS.

## ✨ Features

- **Real-time ISS tracking** using NASA's API
- **Location-based detection** (configurable coordinates)
- **Nighttime filtering** - only notifies when it's dark outside
- **Email notifications** when ISS is overhead
- **Automatic monitoring** - runs continuously in the background
- **Easy configuration** for any location worldwide

## 🚀 How It Works

1. **Fetches ISS position** from the Open Notify API every minute
2. **Checks if ISS is overhead** (within ±5 degrees of your location)
3. **Determines if it's nighttime** using sunrise/sunset API
4. **Sends email notification** when both conditions are met
5. **Repeats the process** continuously

## 📋 Prerequisites

- Python 3.6+
- Gmail account (for sending notifications)
- App password for Gmail (not your regular password)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/iss-overhead-notifier.git
cd iss-overhead-notifier
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your settings:**
   - Copy `config.example.py` to `config.py`
   - Edit `config.py` with your coordinates and email settings

4. **Set up Gmail App Password:**
   - Enable 2-factor authentication on your Gmail account
   - Generate an App Password: [Google Account Settings](https://myaccount.google.com/apppasswords)
   - Use this App Password in your config, not your regular Gmail password

## ⚙️ Configuration

Edit `config.py` with your details:

```python
# Your coordinates (get from Google Maps)
MY_LAT = 51.507351  # London example
MY_LONG = -0.127758

# Email settings
MY_EMAIL = "your.email@gmail.com"
MY_PASSWORD = "your-app-password"  # Gmail App Password
TO_EMAIL = "recipient@gmail.com"   # Can be same as MY_EMAIL
```

## 🏃‍♂️ Usage

**Run once:**
```bash
python iss_tracker.py
```

**Run continuously (recommended):**
```bash
# On Linux/Mac (runs in background)
nohup python iss_tracker.py &

# On Windows (keep terminal open)
python iss_tracker.py
```

**Stop the program:**
- Press `Ctrl+C` in the terminal
- Or close the terminal window

## 📍 Finding Your Coordinates

1. Go to [Google Maps](https://maps.google.com)
2. Right-click on your location
3. Copy the coordinates (latitude, longitude)
4. Update `MY_LAT` and `MY_LONG` in `config.py`

## 📧 Email Setup (Gmail)

1. **Enable 2-Factor Authentication:**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Turn on 2-Step Verification

2. **Create App Password:**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this in `config.py` (not your regular Gmail password)

## 🔧 Customization

- **Change detection range:** Modify the `±5` degrees in `is_iss_overhead()`
- **Adjust check interval:** Change `time.sleep(60)` to different seconds
- **Modify email content:** Edit the message in the `sendmail()` function
- **Add multiple recipients:** Extend the email functionality

## 📊 API Information

- **ISS Position:** [Open Notify ISS API](http://api.open-notify.org/iss-now.json)
- **Sunrise/Sunset:** [Sunrise Sunset API](https://api.sunrise-sunset.org/json)

## 🐛 Troubleshooting

**"Authentication failed" error:**
- Make sure you're using Gmail App Password, not regular password
- Check that 2-factor authentication is enabled

**No notifications received:**
- Verify your coordinates are correct
- Check if ISS actually passes over your location
- Test email settings with the test script

**"Connection error":**
- Check your internet connection
- APIs might be temporarily unavailable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🌟 Fun Facts

- The ISS orbits Earth every ~90 minutes
- It travels at about 17,500 mph (28,000 km/h)
- The ISS is visible to the naked eye and appears as a bright moving star
- Best viewing is during twilight when the sky is dark but ISS is still in sunlight

## 🔮 Future Enhancements

- [ ] Web dashboard for tracking
- [ ] Multiple notification methods (SMS, Discord, Slack)
- [ ] ISS visibility duration prediction
- [ ] Mobile app version
- [ ] Multiple location monitoring
- [ ] Weather integration (cloud cover check)

---

⭐ **If you spot the ISS thanks to this project, please give it a star!** ⭐

*Happy stargazing! 🌌*
