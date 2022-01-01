import discord
from discord.ext import commands
from discord.commands import slash_command

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='smessage',brief="Envoi un message secrétement à quelqu'un !",guild_ids=[665676159421251587])
    async def smessage(self,ctx,member:discord.Member, *,message:str):
        await member.send(message)
        await ctx.respond(f"Ton message a été envoyé !",ephemeral=True)

def setup(bot):
	bot.add_cog(message(bot))
