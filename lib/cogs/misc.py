import discord
from discord.commands import slash_command, user_command, message_command
from discord.commands import Option
from discord.ext import commands

import random
import time
import datetime
from datetime import datetime

from lib.cogs.message import message

from ..db import db

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @user_command(name="Dire coucou",guild_ids=[665676159421251587])
    async def hi(self, interaction, user):
        await interaction.respond(f"{interaction.author.mention} dit coucou à {user.name}!")

    @slash_command(name='random',description='Tirage au sort',guild_ids=[665676159421251587])
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
        

    @message_command(name="Dit au revoir !",guild_ids=[665676159421251587])
    async def aurevoir(self,ctx,message):
        year = str(datetime.now().strftime("%Y"))
        fanette = self.bot.get_user(249970729418752000)
        db.execute("""INSERT INTO guild_stats(guildid,year,no_goodbye_fanette) VALUES(%s,%s,%s) ON CONFLICT(guildid,year) DO UPDATE SET no_goodbye_fanette = guild_stats.no_goodbye_fanette + 1;""",str(ctx.guild.id),year,1)          
        await ctx.respond(f'{fanette.mention} n\'a pas dis au revoir ? Très bien, nous allons lui niquer sa mère.')

def setup(bot):
    bot.add_cog(Misc(bot))
