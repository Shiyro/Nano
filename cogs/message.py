import discord
from discord.ext import commands

class message(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config

    @commands.command(name='smessage',help="Envoi un message secrétement à quelqu'un !")
    async def kick(self,ctx,member:discord.Member, message:str):
        await ctx.message.delete()
        await member.send(message)
