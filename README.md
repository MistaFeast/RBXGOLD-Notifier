# RBXGOLD Rain Notifier

🌧️ Get notified when rain is about to pour on RBXGOLD.com! This Python script monitors the RBXGOLD API for rain events and sends a Discord alert using a webhook.

## Prerequisites

Make sure you have Python 3.7 or later installed on your machine.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rbxgold-rain-notifier.git
   cd rbxgold-rain-notifier
   ```
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Update the Discord webhook URL and rain alert threshold in main.py:
   ```python
   DISCORD_WEBHOOK = "your_discord_webhook_url_here"
   RAIN_ALERT_THRESHOLD = 60  # seconds (adjust if needed)
   ```

## How To Run

Simply execute the following command in your terminal:
```bash
python ./main.py
```
The script will connect to the RBXGOLD API and start monitoring rain events. When a rain is detected, it will send a Discord notification to your webhook.

## Customization

Feel free to customize the Discord alert message, webhook details, and rain alert threshold to suit your preferences. The script is designed to be easily adaptable.

## Credits

* **MistaFeast** - Script author

## Disclaimer

This script is provided as-is. Use it responsibly and at your own risk.
