import discord
from discord.ext import commands
import config
from cogs import kick, event,message, random_cmd, commandes,hub
from cogs.Musique import music

cfg = config.load_config()

#activity = discord.Game(name="!help")
#activity = discord.Streaming(name="!help", url="twitch_url_here")
#activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
activity = discord.Activity(type=discord.ActivityType.watching, name="les étoiles")

bot = commands.Bot(command_prefix=cfg["prefix"], intents = discord.Intents.all(), activity=activity)

COGS = [music.Music, message.message, kick.kick, random_cmd.random_cmd, event.event,commandes.commandes,hub.hub]

def add_cogs(bot):
    for cog in COGS:
        bot.add_cog(cog(bot,cfg))  # Initialize the cog and add it to the bot

def run():
    add_cogs(bot)
    if cfg["token"] == "":
        raise ValueError(
            "No token has been provided. Please ensure that config.toml contains the bot token."
        )
        sys.exit(1)
    bot.run(cfg["token"])

run()
