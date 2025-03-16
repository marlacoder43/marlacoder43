from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, START_FILE, EDIT_START_FILE
from database import load_json, save_json

async def start(client, message):
    user_id = message.chat.id
    users = load_json("users.json", {})

    if str(user_id) not in users:
        users[str(user_id)] = {"first_name": message.from_user.first_name}
        save_json("users.json", users)

    start_data = load_json(START_FILE, {"text": "👋 Salom {first_name}!\n\n🔎 Kino kodini kiriting.", "photo": None})
    formatted_text = start_data["text"].format(first_name=message.from_user.first_name)

    keyboard = None
    if message.from_user.id == ADMIN_ID:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Start xabarini o‘zgartirish", callback_data="edit_start_text")],
            [InlineKeyboardButton("🖼 Start rasmini o‘zgartirish", callback_data="edit_start_photo")]
        ])

    if start_data["photo"]:
        await client.send_photo(user_id, start_data["photo"], caption=formatted_text, reply_markup=keyboard)
    else:
        await client.send_message(user_id, formatted_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("edit_start_text"))
async def edit_start_text(client, callback_query):
    if callback_query.from_user.id != ADMIN_ID:
        return

    await callback_query.message.delete()
    await client.send_message(
        ADMIN_ID, "✍️ Yangi start xabarini yuboring:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_edit")]])
    )
    with open(EDIT_START_FILE, "w") as f:
        f.write("edit_text")

@Client.on_callback_query(filters.regex("cancel_edit"))
async def cancel_edit(client, callback_query):
    os.remove(EDIT_START_FILE)
    await callback_query.message.delete()
    await start(client, callback_query.message)