from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
import asyncio
import random
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("dres_anti_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Cache bot info
bot_user = None

async def get_bot_info(client):
    global bot_user
    if bot_user is None:
        bot_user = await client.get_me()
        print(f"Bot logged in as: {bot_user.first_name} (@{bot_user.username}) - ID: {bot_user.id}")
    return bot_user

@app.on_message(filters.command("kicknopfp") & filters.group)
async def kick_no_profile_picture(client, message):
    await get_bot_info(client)

    # Admin check
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
    except FloodWait as e:
        await message.reply(f"⚠️ Rate limited. Waiting {e.value} seconds...")
        await asyncio.sleep(e.value + 1)
        member = await client.get_chat_member(message.chat.id, message.from_user.id)

    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await message.reply("❌ Only group admins can use this command.")
        return

    await message.reply("🔍 Scanning **all members** for no profile picture...")

    kicked_count = 0
    async for member in client.get_chat_members(message.chat.id):
        user = member.user

        if user.is_bot or user.is_deleted:
            continue
        if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            continue
        if user.id == bot_user.id:
            continue

        if not user.photo:
            try:
                await client.ban_chat_member(message.chat.id, user.id)
                await client.unban_chat_member(message.chat.id, user.id)  # Just kick

                kicked_count += 1
                print(f"No PFP kicked: {user.first_name or 'No Name'} ({user.id}) | Total: {kicked_count}")

                await asyncio.sleep(random.uniform(2, 5))
            except FloodWait as e:
                minutes = e.value // 60 + 1
                await message.reply(f"⚠️ Rate limit. Pausing ~{minutes} min. Kicked so far: {kicked_count}")
                await asyncio.sleep(e.value + 1)
            except Exception as e:
                print(f"Error kicking {user.id}: {e}")

    await message.reply(f"✅ No-PFP scan complete!\nKicked **{kicked_count}** members.")

@app.on_message(filters.command("kickjoined") & filters.group)
async def kick_recent_joiners(client, message):
    await get_bot_info(client)

    # Admin check
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
    except FloodWait as e:
        await message.reply(f"⚠️ Waiting {e.value}s due to rate limit...")
        await asyncio.sleep(e.value + 1)
        member = await client.get_chat_member(message.chat.id, message.from_user.id)

    if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        await message.reply("❌ Only admins can use this command.")
        return

    # Parse hours
    cmd_parts = message.text.split()
    try:
        hours = float(cmd_parts[1]) if len(cmd_parts) > 1 else 3.0
        if not (0.1 <= hours <= 72):
            await message.reply("Please enter hours between 0.1 and 72.")
            return
    except:
        await message.reply("Usage: /kickjoined <hours>\nExample: /kickjoined 2.5\nDefault: 3 hours")
        return

    # Cutoff time in UTC (aware)
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

    await message.reply(f"🔍 Scanning and kicking members who joined in the last **{hours} hours**...")

    kicked_count = 0
    async for member in client.get_chat_members(message.chat.id):
        # Skip if no joined_date
        if not member.joined_date:
            continue

        # Ensure joined_date is UTC-aware
        joined_date = member.joined_date
        if joined_date.tzinfo is None:
            joined_date = joined_date.replace(tzinfo=timezone.utc)
        else:
            joined_date = joined_date.astimezone(timezone.utc)

        # Check if joined recently
        if joined_date > cutoff_time:
            user = member.user

            if user.is_bot or user.is_deleted:
                continue
            if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                continue
            if user.id == bot_user.id:
                continue

            try:
                await client.ban_chat_member(message.chat.id, user.id)
                await client.unban_chat_member(message.chat.id, user.id)  # Remove for permanent ban

                kicked_count += 1
                print(f"Recent joiner kicked: {user.first_name or 'No Name'} ({user.id}) | Joined: {joined_date}")

                await asyncio.sleep(random.uniform(2, 5))
            except FloodWait as e:
                minutes = e.value // 60 + 1
                await message.reply(f"⚠️ Rate limit hit. Pausing ~{minutes} minutes...\nKicked so far: {kicked_count}")
                await asyncio.sleep(e.value + 1)
            except Exception as e:
                print(f"Error kicking recent {user.id}: {e}")

    await message.reply(f"✅ Recent joiners scan complete!\nKicked **{kicked_count}** members who joined in the last {hours} hours.")

print("DresAntiRaidBot is running: /kicknopfp | /kickjoined <hours>")
app.run()