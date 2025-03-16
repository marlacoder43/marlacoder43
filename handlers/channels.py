from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, FORCE_SUB_FILE, EDIT_FORCE_SUB_FILE
from database import load_json, save_json

@Client.on_message(filters.command("kanal") & filters.user(ADMIN_ID))
async def manage_channels(client, message):
    channels = load_json(FORCE_SUB_FILE, [])
    buttons = [[InlineKeyboardButton(f"🚫 O‘chirish - {channel}", callback_data=f"del_{channel}")] for channel in channels]

    if len(channels) < 6:
        buttons.append([InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="add_channel")])

    await client.send_message(
        ADMIN_ID,
        "📢 <b>Majburiy obuna kanallarini boshqarish</b>\n\n📌 Kanal qo‘shish yoki o‘chirish uchun tugmalarni bosing.",
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("add_channel"))
async def request_channel_id(client, callback_query):
    await client.send_message(ADMIN_ID, "🔹 Yangi kanalni @username yoki ID (-100XXXXXXXXXX) shaklida yuboring.")
    with open(EDIT_FORCE_SUB_FILE, "w") as f:
        f.write("add_channel")

@Client.on_message(filters.text & filters.user(ADMIN_ID))
async def add_channel(client, message):
    if not os.path.exists(EDIT_FORCE_SUB_FILE):
        return  

    with open(EDIT_FORCE_SUB_FILE, "r") as f:
        mode = f.read().strip()

    if mode == "add_channel":
        channel = message.text.strip()
        channels = load_json(FORCE_SUB_FILE, [])

        if channel.startswith("@") or channel.startswith("-100"):
            if channel not in channels:
                channels.append(channel)
                save_json(FORCE_SUB_FILE, channels)
                await message.reply_text(f"✅ {channel} kanal majburiy obunaga qo‘shildi!")
            else:
                await message.reply_text("⚠️ Bu kanal allaqachon qo‘shilgan!")
        else:
            await message.reply_text("⚠️ Noto‘g‘ri format! Kanal ID yoki @username yuboring.")

        os.remove(EDIT_FORCE_SUB_FILE)  

@Client.on_callback_query(filters.regex(r"del_(.+)"))
async def remove_channel(client, callback_query):
    channel = callback_query.data.split("_", 1)[1]
    channels = load_json(FORCE_SUB_FILE, [])

    if channel in channels:
        channels.remove(channel)
        save_json(FORCE_SUB_FILE, channels)
        await callback_query.message.edit_text(f"✅ {channel} majburiy obunadan olib tashlandi.")
    else:
        await callback_query.answer("⚠️ Kanal topilmadi!", show_alert=True)