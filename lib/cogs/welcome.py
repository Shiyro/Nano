from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db


class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO users(userid) VALUES(%s) ON CONFLICT DO NOTHING", member.id)
		await self.bot.get_channel(818142776117035038).send(f"Bienvenue sur **{member.guild.name}** {member.mention}!")

	@Cog.listener()
	async def on_member_remove(self, member):
		await self.bot.get_channel(818142776117035038).send(f"{member.display_name} a abandonné le navire !")


def setup(bot):
	bot.add_cog(Welcome(bot))
