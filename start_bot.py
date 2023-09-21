from lib.bot import bot
from dotenv import load_dotenv

VERSION = "2.270823b"

load_dotenv()
bot.run(VERSION)
