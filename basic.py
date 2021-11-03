import discord 
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='?', intents = discord.Intents.all())

class basic(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name='ping',help='Pong !')
    async def ping(self,ctx):
      await ctx.send(f'**Pong!**   <:1440zerosalute:859743676187803668> ')

    @commands.command(name='info',help='Donne les infos du serveur !')
    async def info(self,ctx):
      embed = discord.Embed(title=f"{ctx.guild.name}", description="Un serveur pas comme les autres ", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
      embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
      embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
      embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
      embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
      # embed.set_thumbnail(url=f"{ctx.guild.icon}")
      embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
      
      await ctx.send(embed=embed)
      #embed.set_thumbnail(url=f"{ctx.guild.icon_url}") 

def setup(client):
  client.add_cog(basic(client))

  

