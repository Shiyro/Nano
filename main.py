import discord
from discord.ext import commands
import music
import basic
import help
import random_cmd
import kick
import datetime
import message

token = "ODg4NDUwNTIyNDg1NTEwMTY0.YUS4Bw.MifHENrU37opwofqLsB_zyR38WY"

cogs = [music,help,random_cmd,basic,kick,message]

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

@bot.event
async def on_ready():
  print('\033[32m'"Le bot est pret !"'\033[0m')

@bot.event
async def on_message(message):
  await bot.process_commands(message)
  if not message.author is bot.user:
    if not message.guild: # dm only
      await bot.get_channel(905566642858242049).send(message.content)
    else: # server text channel
      pass
  if 'quoi' in message.content.lower():
    await message.channel.send('Feur ! <:fanette_smug:869876996061147186>')

bot.run(token)