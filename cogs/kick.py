import discord
from discord.ext import commands
import random
import json
from datetime import datetime

random.seed(datetime.now())

class kick(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config

    @commands.command(name='kick',help="Kick quelqu'un secrétement !")
    async def kick(self,ctx,member:discord.Member):
      await ctx.message.delete()
      await member.move_to(None)

    @commands.command(name='rkick',help="Kick quelqu'un aléatoirement !")
    async def random_kick(self,ctx):
      ListeMembres = ctx.guild.members
      Kicked = False

      while not Kicked:
        try:
          Membre = random.randint(0,len(ListeMembres)-1)
          if ListeMembres[Membre].voice == None:
            del(ListeMembres[Membre])
          else:
            await ctx.send(f'{ListeMembres[Membre].mention} tu es l\'élu !')
            await ListeMembres[Membre].move_to(None)
            Kicked = True

        except:
          Kicked = True
