import discord
from discord.ext import commands
import random
import json

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick',brief="Kick quelqu'un secrétement !")
    async def kick(self,ctx,member:discord.Member):
      await ctx.message.delete()
      await member.move_to(None)

    @commands.command(name='rkick',brief="Kick quelqu'un aléatoirement !")
    async def random_kick(self,ctx):
      ListeMembres = ctx.guild.members
      Kicked = False

      while not Kicked and len(ListeMembres)!=0:
          Membre = random.randint(0,len(ListeMembres)-1)
          if ListeMembres[Membre].voice == None:
            del(ListeMembres[Membre])
          else:
            await ctx.send(f'{ListeMembres[Membre].mention} tu es l\'élu !')
            await ListeMembres[Membre].move_to(None)
            Kicked = True

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("kick")

def setup(bot):
	bot.add_cog(kick(bot))
