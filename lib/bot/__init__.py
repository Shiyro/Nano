from asyncio import sleep
from datetime import datetime
from glob import glob

from ..bot import config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord import Intents
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..cogs import birthday
from ..db import db

OWNER_IDS = [238039924178157568]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
cfg=config.load_config()
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"{cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.ready = False
		self.cogs_ready = Ready()

		self.guild = None
		self.TOKEN=cfg["token"]
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)

		super().__init__(command_prefix=cfg["prefix"], owner_ids=OWNER_IDS, intents=Intents().all())

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"{cog} cog loaded")

		print("setup complete")

	def update_db(self):
		db.multiexec("INSERT INTO users(userid) VALUES(%s) ON CONFLICT DO NOTHING",((member.id,) for member in self.guild.members if not member.bot))
		db.commit()

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if not self.ready:
				await ctx.send("Je ne suis pas encore prêt à recevoir des commandes.")
			else:
				await self.invoke(ctx)

	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Quelque chose s'est mal passé.")

		await self.stdout.send("Une erreur est survenu !")
		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("Il manque un ou plusieurs arguments.")

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"Cette commande est en {str(exc.cooldown.type).split('.')[-1]} cooldown. Reessaye dans {exc.retry_after:,.2f} secs.")

		elif hasattr(exc, "original"):
			# if isinstance(exc.original, HTTPException):
			# 	await ctx.send("Unable to send message.")

			if isinstance(exc.original, Forbidden):
				await ctx.send("Je n'ai pas les permissions pour effectuer ca !")

			else:
				raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(665676159421251587)
			self.stdout = self.get_channel(919912122660556870)
			birthday = self.get_cog("Birthday")
			birthday.add_birthday_schedule(self.scheduler)
			self.scheduler.start()

			self.update_db()

			while not self.cogs_ready.all_ready():
				await sleep(0.2)

			await self.stdout.send("En ligne !")
			self.ready = True
			print("Bot ready")

			meta = self.get_cog("Meta")
			await meta.set()

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)
			if not message.guild: # si le bot recois en pm
				await self.get_channel(905566642858242049).send(message.content)
			else: #Message sur le serveur
				pass
			if 'quoi' in message.content.lower():
				await message.channel.send('**Feur !**')

bot = Bot()
