from datetime import datetime, timedelta
from platform import python_version
from time import time

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed, Color
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command,slash_command
import discord
from psutil import Process, virtual_memory

from ..db import db


class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_command(name="ping",description="Retourne la latence avec le bot")
	async def ping(self, interaction):
		await interaction.defer()
		start = time()
		message = await interaction.followup.send(f"Pong! Latence DWSP: {self.bot.latency*1000:,.0f} ms.",ephemeral=True)
		end = time()

		await message.edit(content=f"Pong! Latence DWSP: {self.bot.latency*1000:,.0f} ms. Temps de reponse: {(end-start)*1000:,.0f} ms.")

	@slash_command(name='info',description='Donne les infos du serveur !')
	async def info(self, interaction):
		embed = discord.Embed(title=f"{interaction.guild.name}", description="Un serveur pas comme les autres ", timestamp=datetime.utcnow())
		embed.add_field(name="Serveur crée à :", value=f"{interaction.guild.created_at}")
		embed.add_field(name="Appartient a", value=f"{interaction.guild.owner}")
		embed.add_field(name="ID Serveur", value=f"{interaction.guild.id}")
		embed.set_thumbnail(url=f"{interaction.guild.icon.url}")
		await interaction.response.send_message(embed=embed,ephemeral=True)

	@slash_command(name="stats",description="Affiche les infos du bot.")
	async def show_bot_stats(self, interaction):
		embed = Embed(title="Stats du bot",
					  colour=interaction.user.colour,
					  timestamp=datetime.utcnow())
		embed.set_thumbnail(url=self.bot.user.avatar.url)

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
			("Py-cord version", discord_version, True),
			("Uptime", uptime, True),
			("CPU time", cpu_time, True),
			("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
			("Users", f"{self.bot.guild.member_count:,}", True)
		]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await interaction.response.send_message(embed=embed,ephemeral=True)

	@slash_command(name="shutdown", description="Arrête le bot.")
	async def shutdown(self, interaction):
		await interaction.response.send_message("Arret du bot...")
		db.commit()
		self.bot.scheduler.shutdown()
		await self.bot.close()
		
def setup(bot):
	bot.add_cog(Meta(bot))