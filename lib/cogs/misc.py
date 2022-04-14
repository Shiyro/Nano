import discord
from discord.commands import slash_command, user_command, message_command
from discord.commands import Option
from discord.ext import commands

import random
import time
import datetime
from datetime import datetime

from ..db import db

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @user_command(name="Dire coucou")
    async def hi(self, interaction, user):
        await interaction.respond(f"{interaction.author.mention} dit coucou à {user.name}!")

    @slash_command(name='random',description='Tirage au sort')
    async def random(
    self,
    interaction,
    type: Option(str, "Choisi le type de tirage au sort", choices=["Liste", "Nombre", "Rôle"]),
    valeur: Option(str, "Entrez le(s) valeur(s).")
    ):
        valeur = valeur.split(";")
        if type=="Nombre":
            if valeur[0].isnumeric() and len(valeur)==1:
                await interaction.response.send_message(str(random.randint(1,int(valeur[0]))))
            else:
                await interaction.response.send_message("Merci de rentrer un nombre valide.",ephemeral=True)
        elif type=="Rôle":
            role = valeur[0].replace("<@&","")
            role = role.replace(">","")
            if role.isnumeric():
                role = interaction.guild.get_role(int(role))
            else:
                role = None
            if role is not None and len(valeur)==1:
                membre = random.choice(role.members)
                await interaction.response.send_message(membre.name)
            else:
                await interaction.response.send_message("Merci de rentrer un role valide.",ephemeral=True)
        elif type=="Liste":
            await interaction.response.send_message(random.choice(valeur))

    @slash_command(name='smessage',brief="Envoi un message secrétement à quelqu'un !")
    async def smessage(self,ctx,member:discord.Member, *,message:str):
        await member.send(message)
        await ctx.respond(f"Ton message a été envoyé !",ephemeral=True)

def setup(bot):
    bot.add_cog(Misc(bot))
