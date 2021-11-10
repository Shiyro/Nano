import discord
from discord.ext import commands

class event(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config

    @commands.Cog.listener()
    async def on_ready(self):
      print('\033[32m'"Le bot est pret !"'\033[0m')

    @commands.Cog.listener()
    async def on_message(self,message):
      if not message.author is self.client.user: #Check si l'auteur du message est pas le bot
        if not message.guild: # si le bot recois en pm
          await self.client.get_channel(905566642858242049).send(message.content)
        else: #Message sur le serveur
          pass
      if 'quoi' in message.content.lower():
        await message.channel.send('Feur ! <:fanette_smug:869876996061147186>')
