import discord
from discord.ext import commands
from discord.commands import slash_command
import random

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='kick',description="Kick quelqu'un qui n'en saura rien !")
    async def kick(self,ctx,member:discord.Member):
        await ctx.respond(f"Tu as kick {member.mention}",ephemeral=True)
        await member.move_to(None)

    @slash_command(name='rkick',description="Kick quelqu'un aléatoirement, à defaut de pouvoir faire une roulette russe virtuelle !")
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

def setup(bot):
	bot.add_cog(kick(bot))