from datetime import datetime, timedelta
from platform import python_version
from time import time

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed, Color
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command
import discord
from psutil import Process, virtual_memory

from ..db import db


class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot
		self._message = "listening du bullshit"
		bot.scheduler.add_job(self.set, CronTrigger(second=0))

	@property
	def message(self):
		return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

	@message.setter
	def message(self, value):
		if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
			raise ValueError("Invalid activity type.")

		self._message = value

	async def set(self):
		_type, _name = self.message.split(" ", maxsplit=1)

		await self.bot.change_presence(activity=Activity(name=_name, type=getattr(ActivityType, _type, ActivityType.playing)))

	@command(name="setactivity", brief="Change l'activité du bot")
	async def set_activity_message(self, ctx, *, text: str):
		self.message = text
		await self.set()

	@command(name="ping",brief="Retourne la latence avec le bot")
	async def ping(self, ctx):
		start = time()
		message = await ctx.send(f"Pong! Latence DWSP: {self.bot.latency*1000:,.0f} ms.")
		end = time()

		await message.edit(content=f"Pong! Latence DWSP: {self.bot.latency*1000:,.0f} ms. Temps de reponse: {(end-start)*1000:,.0f} ms.")

	@command(name='info',brief='Donne les infos du serveur !')
	async def info(self,ctx):
		embed = discord.Embed(title=f"{ctx.guild.name}", description="Un serveur pas comme les autres ", timestamp=datetime.utcnow())
		embed.add_field(name="Serveur crée à :", value=f"{ctx.guild.created_at}")
		embed.add_field(name="Appartient a", value=f"{ctx.guild.owner}")
		embed.add_field(name="Région :", value=f"{ctx.guild.region}")
		embed.add_field(name="ID Serveur", value=f"{ctx.guild.id}")
		# embed.set_thumbnail(url=f"{ctx.guild.icon}")
		embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
		await ctx.send(embed=embed)
		#embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

	@command(name="stats",brief="Affiche les infos du bot.")
	async def show_bot_stats(self, ctx):
		embed = Embed(title="Stats du bot",
					  colour=ctx.author.colour,
					  thumbnail=self.bot.user.avatar_url,
					  timestamp=datetime.utcnow())

		proc = Process()
		with proc.oneshot():
			uptime = timedelta(seconds=time()-proc.create_time())
			cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
			mem_total = virtual_memory().total / (1024**2)
			mem_of_total = proc.memory_percent()
			mem_usage = mem_total * (mem_of_total / 100)

		fields = [
			("Bot version", self.bot.VERSION, True),
			("Python version", python_version(), True),
			("discord.py version", discord_version, True),
			("Uptime", uptime, True),
			("CPU time", cpu_time, True),
			("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
			("Users", f"{self.bot.guild.member_count:,}", True)
		]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@command(name="shutdown", brief="Arrete le bot.")
	async def shutdown(self, ctx):
		await ctx.send("Arret du bot...")

		with open("./data/banlist.txt", "w", encoding="utf-8") as f:
			f.writelines([f"{item}\n" for item in self.bot.banlist])

		db.commit()
		self.bot.scheduler.shutdown()
		await self.bot.logout()

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("meta")


def setup(bot):
	bot.add_cog(Meta(bot))
