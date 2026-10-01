import asyncio
import random
import aiohttp
from TikTokLive import TikTokLiveClient
from telegram import Bot

TELEGRAM_TOKEN = "8421996960:AAEVP7TVfbNgFqfIj3bcXkVMpW2aEpZsbNk"
CHANNEL_ID = "@ajinxaxa"

bot = Bot(token=TELEGRAM_TOKEN)

KEYWORDS = ["sandik", "hediye", "pk", "yayin", "pubg", "brawlstars", "roblox", "kesfet", "live"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

async def fetch_live_users():
    found_users = set()
    async with aiohttp.ClientSession(headers=headers) as session:
        for kw in random.sample(KEYWORDS, 4):
            try:
                url = f"https://www.tiktok.com/api/search/general/full/?keyword={kw}&offset=0"
                async with session.get(url, timeout=3) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for item in data.get("data", []):
                            u = item.get("item", {}).get("author", {}).get("uniqueId")
                            if u: found_users.add(u)
            except: pass
    return list(found_users)

async def check_single_stream(username):
    try:
        client = TikTokLiveClient(unique_id=username)
        @client.on("envelope")
        async def on_envelope(event):
            msg = (
                f"🔥 **CLOUD SANDIK BOTU V1**\n\n"
                f"• **Kullanıcı:** `@{username}`\n"
                f"• 🔗 **Yayın Linki:** https://www.tiktok.com/@{username}/live\n\n"
                f"⚡ *Hemen girip sandığı kapın!*"
            )
            await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="Markdown")
            print(f"🎯 Sandık Yakalandı: @{username}")

        task = asyncio.create_task(client.start())
        await asyncio.sleep(2.5)
        await client.disconnect()
    except: pass

async def main():
    scanned = set()
    while True:
        users = await fetch_live_users()
        if not users:
            users = ["pubgmobile", "brawlstars", "roblox", "tiktoklive"]
            
        for i in range(0, len(users), 8):
            chunk = users[i:i + 8]
            tasks = [check_single_stream(u) for u in chunk if u not in scanned]
            for u in chunk: scanned.add(u)
            if len(scanned) > 1000: scanned.clear()
            if tasks: await asyncio.gather(*tasks)
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
          
