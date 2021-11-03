import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bot.command()
    async def aide(ctx): 
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

def setup(client):
  client.add_cog(help(client))