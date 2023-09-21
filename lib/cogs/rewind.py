import datetime
from datetime import datetime
from datetime import date
import random

import discord
from discord.ext.commands import Cog
from discord.commands import slash_command, message_command
from discord.ext import commands
from discord.ui import Button, View

from discord import Embed, File

from apscheduler.triggers.cron import CronTrigger

from ..db import db

class RewindButton(Button):
	def __init__(self,bot):
		super().__init__(label="Découvrir", style=discord.ButtonStyle.primary)
		self.bot = bot
		self.rewind_year = str(datetime.now().strftime("%Y"))
		self.thumbnail = []


	def get_embeds(self,userid):
		embeds = []
		###VOICE TIME###
		if(result := db.field("SELECT voice_channel_time FROM users_stats WHERE userid=%s AND year=%s;",userid,self.rewind_year)) is not None:
			file = File("data/images/desk_icon.png", filename="desk_icon.png")
			embed=Embed(title="Rewind!", description=f"Tu as discuté de plein de choses avec tes amis !", color=0xC2B2EB)
			embed.set_thumbnail(url="attachment://desk_icon.png")
			embed.add_field(name="Temps passé en vocal :",value=f"{round(result/60,1)} heures")
			embed.set_footer(text="Fait avec amour par Shiyro")
			embeds.append(embed)
			self.thumbnail.append(file)

		###MESSAGE SENT###
		if(result := db.field("SELECT message_sent FROM users_stats WHERE userid=%s AND year=%s;",userid,self.rewind_year)) is not None:
			file = File("data/images/paper_plane_icon.png", filename="paper_plane_icon.png")
			embed=Embed(title="Rewind!", description=f"Tu vas surement avoir besoin d'un nouveau clavier...", color=0xB2E7F1)
			embed.set_thumbnail(url="attachment://paper_plane_icon.png")
			embed.add_field(name="Nombre de messages envoyés :",value=f"{result} messages")
			embed.set_footer(text="Fait avec amour par Shiyro")
			embeds.append(embed)
			self.thumbnail.append(file)

		###MUSIC PLAYED###
		if(result := db.field("SELECT music_played FROM users_stats WHERE userid=%s AND year=%s;",userid,self.rewind_year)) is not None:
			file = File("data/images/music_note_icon.png", filename="music_note_icon.png")
			embed=Embed(title="Rewind!", description=f"Tu as fait péter le mur du son !", color=0x9781DD)
			embed.set_thumbnail(url="attachment://music_note_icon.png")
			embed.add_field(name="Nombre de musiques jouées :",value=f"{result} musiques")
			embed.set_footer(text="Fait avec amour par Shiyro")
			embeds.append(embed)
			self.thumbnail.append(file)

		###FEUR###
		if(result := db.field("SELECT feur FROM users_stats WHERE userid=%s AND year=%s;",userid,self.rewind_year)) is not None:
			file = File("data/images/cat_icon.png", filename="cat_icon.png")
			embed=Embed(title="Rewind!", description=f"Tu retiendras donc jamais la leçon...", color=0xE8C2D8)
			embed.set_thumbnail(url="attachment://cat_icon.png")
			embed.add_field(name="Nombre de fois où Nano! a repondu 'Feur' :",value=f"{result} fois")
			embed.set_footer(text="Fait avec amour par Shiyro")
			embeds.append(embed)
			self.thumbnail.append(file)

		###MOST MENTIONED###
		if(result := db.field("select mentioned_user,number_of_mentions from users_mentions where userid=%s and year=%s order by number_of_mentions desc;",userid,self.rewind_year)) is not None:
			result = self.bot.get_user(result)
			file = File("data/images/happy_licorn_icon.png", filename="happy_licorn_icon.png")
			embed=Embed(title="Rewind!", description=f"Bah alors {self.bot.get_user(userid).name}, tu simp sur {result.name} ?", color=0xF4DAB5)
			embed.set_thumbnail(url="attachment://happy_licorn_icon.png")
			embed.add_field(name="La personne que tu as le plus mentionnée :",value=f"{result.mention}")
			embed.set_footer(text="Fait avec amour par Shiyro")
			embeds.append(embed)
			self.thumbnail.append(file)

		self.thumbnail = iter(self.thumbnail)
		return embeds

	async def callback(self,interaction):
		replied = False
		print(f"{interaction.user.name} à cliqué sur le rewind !")
		await interaction.response.edit_message(delete_after=0)
		for embed in self.get_embeds(interaction.user.id):
			await interaction.channel.send(embed=embed,file=next(self.thumbnail))

class Rewind(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def send_rewind(self):
		embed=Embed(title="**Rewind!**", description="Ton récapitulatif annuel est disponible.\nClique sur le bouton pour le découvrir !", color=0x20b6b6)
		embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4869/4869759.png")
		embed.set_footer(text="Fait avec amour par Shiyro")

		users = db.records("SELECT userid FROM users_stats where year=%s",str(datetime.now().strftime("%Y")))
		for user in users:
			user = self.bot.get_user(user[0])
			await user.send(embed=embed,view=View(RewindButton(self.bot),timeout=None))

	def add_rewind_schedule(self,sched):
		sched.add_job(self.send_rewind, CronTrigger(month=12,day=31,hour=22,minute=0,second=0))


def setup(bot):
	bot.add_cog(Rewind(bot))
