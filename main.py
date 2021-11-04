import discord
from discord.ext import commands
import musique
import commandes
import random_cmd
import kick
import datetime
import message
import event

token = "ODg4NDUwNTIyNDg1NTEwMTY0.YUS4Bw.KeUrMZ4GEUTRJFFP5WVTR_jg7hE"

cogs = [musique,random_cmd,commandes,kick,message,event]

#activity = discord.Game(name="!help")
#activity = discord.Streaming(name="!help", url="twitch_url_here")
#activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
activity = discord.Activity(type=discord.ActivityType.watching, name="les étoiles")

bot = commands.Bot(command_prefix='?', intents = discord.Intents.all(), activity=activity)

for i in range(len(cogs)):
  print("Loading : "+str(cogs[i]))
  cogs[i].setup(bot)

async def start_bot():
  await bot.start(token)

bot.run(token)

#test
