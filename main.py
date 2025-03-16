from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start import start
from handlers.movies import upload_movie, send_movie
from handlers.channels import manage_channels, add_channel, remove_channel
from handlers.broadcast import broadcast_message, send_broadcast, cancel_broadcast
from handlers.stats import bot_stats

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bot.add_handler(start)
bot.add_handler(upload_movie)
bot.add_handler(send_movie)
bot.add_handler(manage_channels)
bot.add_handler(add_channel)
bot.add_handler(remove_channel)
bot.add_handler(broadcast_message)
bot.add_handler(send_broadcast)
bot.add_handler(cancel_broadcast)
bot.add_handler(bot_stats)

bot.run()