import discord
from discord.commands import slash_command, user_command, message_command
from discord.ext import commands

import random
import time
import datetime
from datetime import datetime

from ..db import db

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @user_command(name="Dire coucou",guild_ids=[665676159421251587])
    async def hi(self,ctx, user):
        await ctx.respond(f"{ctx.author.mention} dit coucou à {user.name}!")

    @commands.command(name='random',description='Obtient un chiffre entre 1 et la valeur max entré')
    async def random(self,ctx,type,*args):
      embed=discord.Embed(title="", description="Roulement de tambours.... ! ", color=0xffffff)
      await ctx.send(embed=embed)
      time.sleep(2.5)
      embed=discord.Embed(title='', description='', color=0xffffff)
      if type=="valeur":
          embed.add_field(name="Résultat :",value=(str(random.randint(1,int(args[0])))+" !"))
      elif type=="role":
          role = ctx.guild.get_role(ctx.message.raw_role_mentions[0])
          membres = role.members
          embed.add_field(name="Résultat :",value=(membres[random.randint(0,len(membres)-1)].name +" !"))
      else:
          embed.add_field(name="Résultat :",value=(args[random.randint(0,len(args)-1)]+" !"))
      await ctx.send(embed=embed)

    @message_command(name="Dit au revoir !",guild_ids=[665676159421251587])
    async def aurevoir(self,ctx,message):
    	year = str(datetime.now().strftime("%Y"))
    	fanette = self.bot.get_user(249970729418752000)
    	db.execute("""INSERT INTO guild_stats(guildid,year,no_goodbye_fanette)
    				  VALUES(%s,%s,%s)
    				  ON CONFLICT(guildid,year)
    				  DO UPDATE SET no_goodbye_fanette = guild_stats.no_goodbye_fanette + 1;""",str(ctx.guild.id),year,1)

    	await ctx.respond(f'{fanette.mention} n\'a pas dis au revoir ? Très bien, nous allons lui niquer sa mère.')

def setup(bot):
    bot.add_cog(Misc(bot))
