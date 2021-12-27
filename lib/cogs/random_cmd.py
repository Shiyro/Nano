import discord
from discord.ext import commands
import random
import time

class random_cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='random',brief='Obtient un chiffre entre 1 et la valeur max entré')
    async def random(self,ctx,*args):
      embed=discord.Embed(title="", description="Roulement de tambours.... ! ", color=0xffffff)
      await ctx.send(embed=embed)
      time.sleep(2.5)

      embed=discord.Embed(title='', description='', color=0xffffff)
      if len(args)==1 and args[0].isnumeric():
          embed.add_field(name="Résultat :",value=(str(random.randint(1,int(args[0])))+" !"))
      elif len(args)==1 and len(ctx.message.raw_role_mentions)==1:
          role = ctx.guild.get_role(ctx.message.raw_role_mentions[0])
          membres = role.members
          embed.add_field(name="Résultat :",value=(membres[random.randint(0,len(membres)-1)].name +" !"))
      else:
          embed.add_field(name="Résultat :",value=(args[random.randint(0,len(args)-1)]+" !"))
      await ctx.send(embed=embed)


    @commands.command(name='piece', brief='Pile ou face ?')
    async def piece(self,ctx):
      embed=discord.Embed(title="", description="Retombée de piece... !", color=0xffffff)
      await ctx.send(embed=embed)
      time.sleep(2.5)
      rng = random.randint(0,1)
      if rng == 0:
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name="Résultat :",value= "PɩꙆᥱ !")
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name="Résultat :",value="Fᥲᥴᥱ !")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("random_cmd")

def setup(bot):
	bot.add_cog(random_cmd(bot))
