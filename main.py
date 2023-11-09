import asyncio
import json
import pytz
import requests
import websockets
from datetime import datetime

# Constants
DISCORD_WEBHOOK = ""
RBXGOLD_API_URL = "wss://api.rbxgold.com/socket.io/?EIO=4&transport=websocket"
RAIN_ALERT_THRESHOLD = 60  # seconds

def sendAlert(data, time):
    webhook_body = {
        "content": "@everyone",
        "username": "RBXGOLD Rain Notifier",
        "avatar_url": "https://static.rbxgold.com/media/favicon.png",
        "url": "https://rbxgold.com/",
        "embeds": [
            {
                "title": f"Rain Incoming! [${data[1]["documents"][0]["evAmount"]}]",
                "description": f"Rain in about {str(int(time))} seconds! Be quick!",
                "image": {
                    "url": "https://roblox-static.s3.amazonaws.com/media/site-banner.png"
                },
                "footer": {
                    "text": "Made by MistaFeast"
                }
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK, data=json.dumps(webhook_body), headers={"Content-Type": "application/json"})

def getCurTime():
    return int(datetime.now(pytz.timezone("US/Eastern")).timestamp())

def convToEst(date):
    return int(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("US/Eastern")).timestamp())

async def main():
    active = False
    curtime = None
    async with websockets.connect(RBXGOLD_API_URL) as ws:
        while True:
            if not active:
                curtime = getCurTime()
            try:
                response = await ws.recv()
                if response.startswith("0"):
                    await ws.send("40")
                elif response == "2":
                    await ws.send("3")
                elif response.startswith('42["rain-value-stream"'):
                    data = json.loads(response[2:])
                    if "endDate" in data[1]["documents"][0]:
                        time = convToEst(data[1]["documents"][0]["endDate"]) - curtime
                        if time <= RAIN_ALERT_THRESHOLD and not active:
                            sendAlert(data, time)
                            active = True
                            curtime = getCurTime() + RAIN_ALERT_THRESHOLD
                    else:
                        active = False
                await asyncio.sleep(1)
                await ws.send('42["rain-ping"]')

                # Tag this print out if you want, it was just for testing but isnt essential to be ran
                print(response)
            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket connection closed due to an internal error or server shutdown.")
                break
            except websockets.exceptions.ConnectionClosedOK:
                print("Server forced restart. WebSocket connection reestablishing...")
                await asyncio.sleep(10)
                asyncio.run(main())
            except KeyboardInterrupt:
                print("Program terminated by the user (KeyboardInterrupt).")
                break

if __name__ == "__main__":
    asyncio.run(main())
