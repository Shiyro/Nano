import discord
from discord.ext import commands
import random
from datetime import datetime
import time

bot = commands.Bot(command_prefix='?')
random.seed(datetime.now())


users=["Shiyro", "Inkukhus", "Fanette", "Sonny", "Logan","Rémi"]
#users=["Logan"]

class random_cmd(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config

    @commands.command(name='bg',help='Vous ? Nan je rigole c\'est random')
    async def bg(self,ctx):
      lpb=users[random.randint(0,len(users)-1)]
      if lpb == "Fanette":
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name="Belle gosse :",value=(lpb+ " c'est la plus belle ! ᙀωᙀ <:Kiss02:842831517537140736>"))
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name="Beau gosse :",value=(lpb+ " c'est le plus beau ! ᙀωᙀ <:Kiss02:842831517537140736>"))
        await ctx.send(embed=embed)

    @commands.command(name='loser',help='Vous ? Oui mais malheuresement c\'est random')
    async def loser(self,ctx):
       loser=users[random.randint(0,len(users)-1)]
       if loser == "Fanette":
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name=" Loseuse :",value=(loser+ " est une big loseuse ! <:guraeheh:866727311540748348>"))
        await ctx.send(embed=embed)
       else:
        embed=discord.Embed(title="", description="", color=0xffffff)
        embed.add_field(name=" Loser :",value=(loser+ " est un big loser ! <:guraeheh:866727311540748348>"))
        await ctx.send(embed=embed)

    @commands.command(name='random',help='Obtient un chiffre entre 1 et la valeur entré')
    async def random(self,ctx,max):
      embed=discord.Embed(title="", description="Roulement de tambours.... ! ", color=0xffffff)
      await ctx.send(embed=embed)
      time.sleep(2.5)
      embed=discord.Embed(title="", description="", color=0xffffff)
      embed.add_field(name="Résultat :",value= (str(random.randint(1,int(max)))+" !"))
      await ctx.send(embed=embed)

    @commands.command(name='piece', help='Pile ou face ?')
    async def piece(self,ctx,):
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
