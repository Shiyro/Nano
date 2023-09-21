import datetime
from datetime import datetime
from datetime import date
import random

from discord.ext.commands import Cog
from discord import Embed,File
from discord.ext.commands import slash_command

from apscheduler.triggers.cron import CronTrigger

from ..db import db

class Birthday(Cog):
	def __init__(self, bot):
		self.bot = bot

	@slash_command(name="anniv",description="Défini ton anniversaire au format DD/MM/YYYY")
	async def set_birthday(self, ctx, date):
		try:
			date_object = datetime.strptime(date,"%d/%m/%Y").date()
			db.execute("UPDATE users SET birthday=%s WHERE userid=%s;",date_object,str(ctx.user.id))
			db.commit()
			await ctx.response.send_message(f'Ton anniversaire à été defini au {date}',ephemeral=True)
		except ValueError:
			await ctx.response.send_message("Merci de rentrer une date au format DD/MM/YYYY.",ephemeral=True)

	def add_birthday_schedule(self,sched):
		sched.add_job(self.send_birthday, CronTrigger(hour=8,minute=0,second=0))

	async def send_birthday(self):

		file = File("data/images/birthday_cake_icon.png", filename="birthday_cake_icon.png")

		def get_embed(self,age):
			embed=Embed(title="**Joyeux anniversaire !** :birthday:", description=get_message(self,age), color=0xFFDCB6)
			embed.set_thumbnail(url="attachment://birthday_cake_icon.png")
			embed.set_footer(text="Fait avec amour par Shiyro")
			return embed

		def get_message(self,age):
			birthday_message = [
			f"Tu as level up !\nTu es désormais niveau **{age}**",
			f"Félicitations, tu as survécu une année de plus.\nProfite bien de cette nouvelle année, ça pourrait être la dernière...",
			f"Un jour n'est pas assez long pour célébrer ton anniversaire.\nOn devrait célébrer le tient pendant une semaine entière !",
			f"Une année de plus te rapproche de la mort...",
			f"Tu as **{age}** ans !\nTant de bougies pour un si petit gateau...",
			f"Je connais beaucoup de célébrités qui sont nées le même jour que le tien…\nDommage que tu n’en sois pas une.",
			f"Tu as **{age}** ans !\nJe pense que tu es devenu assez mature pour ne pas être intéressé par les choses matérialistes.\nComme les cadeaux... ",
			f"Les hommes vieillissent comme du vin, et les femmes vieillissent comme du lait...",
			f"À la seule personne que je sauverai en cas d’invasion de zombies.\nJoyeux anniversaire !",
			f"Désolé que tu aies besoin de faire dérouler tout le menu sur les sites web pour sélectionner ton année de naissance.\nJoyeux anniversaire",
			f"Je n’arrive pas à me souvenir de ton âge,\nje m’en fous d’ailleurs.",
			f"Il commence à faire de plus en plus chaud ici ou bien, ce sont juste les bougies sur ton gâteau.",
			f"Je voulais t’offrir un magnifique cadeau, mais malheureusement je n’ai pas réussi à le faire passer par l’écran de l'ordinateur.",
			f"Oublie le passé,\ntu ne peux plus le changer.\nOublie aussi le présent,\nje t’en ai pas acheté !",
			f"Joyeux anniversaire ! Encore un an de plus et tu seras parfait !",
			f"Il paraît que la perfection n’existe pas sur Terre …\nMais alors dis-moi d’où viens-tu ?",
			f"Joyeux anniversaire, une année de plus vers le cimetière"
			]
			return random.choice(birthday_message)

		db_result = db.records("""SELECT userid,birthday
								  FROM users
                                  WHERE
								  	DATE_PART('day', birthday) = date_part('day', CURRENT_DATE)
								  AND
								  	DATE_PART('month', birthday) = date_part('month', CURRENT_DATE);""")
		for dbuser in db_result:
			user = self.bot.get_user(dbuser[0])
			age = int(date.today().strftime("%Y")) - int(dbuser[1].strftime("%Y"))
			await user.send(file=file,embed=get_embed(self,age))


def setup(bot):
	bot.add_cog(Birthday(bot))
