from pyrogram import Client, filters
from config import ADMIN_ID
from database import load_json

@Client.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def bot_stats(client, message):
    users = load_json("users.json", {})
    await client.send_message(
        ADMIN_ID,
        f"📊 Bot foydalanuvchilari soni: {len(users)}\n\n🆔 Ro‘yxat:\n" +
        "\n".join([f"{uid} - {info['first_name']}" for uid, info in users.items()])
    )