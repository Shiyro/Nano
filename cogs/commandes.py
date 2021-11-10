import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='?', intents = discord.Intents.all())

class commandes(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config

    @commands.command(name='ping',help='Pong !')
    async def ping(self,ctx):
      await ctx.send(f'**Pong!**   <:1440zerosalute:859743676187803668> ')

    @commands.command(name='info',help='Donne les infos du serveur !')
    async def info(self,ctx):
      embed = discord.Embed(title=f"{ctx.guild.name}", description="Un serveur pas comme les autres ", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
      embed.add_field(name="Serveur crée à :", value=f"{ctx.guild.created_at}")
      embed.add_field(name="Appartient a", value=f"{ctx.guild.owner}")
      embed.add_field(name="Région :", value=f"{ctx.guild.region}")
      embed.add_field(name="ID Serveur", value=f"{ctx.guild.id}")
      # embed.set_thumbnail(url=f"{ctx.guild.icon}")
      embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
      await ctx.send(embed=embed)
      #embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

    @commands.command(name='aide',help='aide')
    async def aide(self,ctx):
        embed=discord.Embed(title="Liste des Commandes ", description="Voici la liste des commandes disponible  avec Miguel", color=0xffffff)
        embed.add_field(name="- ?play (url)",value= "Permet de jouer une musique à partir de URL", inline=True)
        embed.add_field(name="- ?disconnect", value="Déconnexion du bot du ᘎOᙅO", inline=True)
        embed.add_field(name="- ?quoi", value="Il vous répondra la meilleur réplique de Fanette", inline=True)
        embed.add_field(name="- ?bg", value="Vous ?, Nan je rigole c'est random", inline=True)
        embed.add_field(name="- ?random (max)", value="Obtient un chiffre entre 1 et la valeur entré", inline=True)
        embed.add_field(name="- ?loser", value="Vous ?,Oui mais malheuresement c'est random", inline=True)
        embed.add_field(name="- ?piece", value="Plutôt Pile ou Face ?", inline=True)
        embed.add_field(name="- ?ping", value="Pong !", inline=True)
        embed.set_footer(text="Sonny / Shiyro")
        await ctx.send(embed=embed)
