import asyncio
import time
from playwright.async_api import async_playwright
import requests
import os

URL = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-2/ET00474271"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LAST_STATE = None
END_TIME = time.time() + (36 * 60 * 60)

def notify(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

async def check():
    global LAST_STATE
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        button = await page.locator("button").first.text_content()

        if LAST_STATE and button.strip() != LAST_STATE:
            notify(f"🚨 Button changed! Now: {button.strip()}")
            exit()

        LAST_STATE = button.strip()
        await browser.close()

async def main():
    while time.time() < END_TIME:
        await check()
        await asyncio.sleep(30)

asyncio.run(main())
