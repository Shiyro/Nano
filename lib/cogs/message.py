import discord
from discord.ext import commands

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='smessage',brief="Envoi un message secrétement à quelqu'un !")
    async def kick(self,ctx,member:discord.Member, message:str):
        await ctx.message.delete()
        await member.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("message")

def setup(bot):
	bot.add_cog(message(bot))
