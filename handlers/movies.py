from pyrogram import Client, filters
from config import ADMIN_ID, MOVIE_CHANNEL, STORAGE_CHANNEL, LIST_FILE
from database import load_json, save_json

@Client.on_message(filters.video & filters.user(ADMIN_ID))
async def upload_movie(client, message):
    try:
        forwarded_message = await client.forward_messages(
            chat_id=STORAGE_CHANNEL,
            from_chat_id=message.chat.id,
            message_ids=message.id
        )

        forwarded_message_id = forwarded_message.id if hasattr(forwarded_message, "id") else forwarded_message[0].id
        movie_list = load_json(LIST_FILE, [])

        if forwarded_message_id not in movie_list:
            movie_list.append(forwarded_message_id)
            save_json(LIST_FILE, movie_list)

        await message.reply_text(f"🚀 Kino yuklandi!\n\n#️⃣ Kino kodi: {forwarded_message_id}")
    except Exception as e:
        await message.reply_text(f"❌ Xatolik: {str(e)}")

@Client.on_message(filters.text & filters.private)
async def send_movie(client, message):
    movie_code = message.text.strip()
    if not movie_code.isdigit():
        return  

    movie_list = load_json(LIST_FILE, [])
    if int(movie_code) in movie_list:
        try:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=MOVIE_CHANNEL,
                message_id=int(movie_code),
                caption="🎬 Siz so‘ragan kino topildi!"
            )
        except:
            await message.reply_text("❌ Kino topilmadi yoki xatolik yuz berdi!")
    else:
        await message.reply_text("❌ Bunday kino kodi topilmadi!")