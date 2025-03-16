from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, EDIT_BROADCAST_FILE
from database import load_json

@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_message(client, message):
    users = load_json("users.json", {})
    if not users:
        await client.send_message(ADMIN_ID, "⚠️ Hech qanday foydalanuvchi yo‘q!")
        return

    await client.send_message(
        ADMIN_ID,
        "📨 Yangi xabarni yozing va botga yuboring.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_broadcast")]
        ])
    )
    with open(EDIT_BROADCAST_FILE, "w") as f:
        f.write("broadcast")

@Client.on_message(filters.text & filters.user(ADMIN_ID))
async def send_broadcast(client, message):
    if os.path.exists(EDIT_BROADCAST_FILE):
        with open(EDIT_BROADCAST_FILE, "r") as f:
            mode = f.read().strip()

        if mode == "broadcast":
            users = load_json("users.json", {})
            for user_id in users:
                try:
                    await client.send_message(int(user_id), message.text)
                except:
                    continue

            os.remove(EDIT_BROADCAST_FILE)
            await message.reply_text("✅ Xabar jo‘natildi!")

@Client.on_callback_query(filters.regex("cancel_broadcast"))
async def cancel_broadcast(client, callback_query):
    if os.path.exists(EDIT_BROADCAST_FILE):
        os.remove(EDIT_BROADCAST_FILE)
        await callback_query.message.edit_text("❌ Xabar yuborish bekor qilindi!")