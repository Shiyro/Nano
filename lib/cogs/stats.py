import discord
from discord.ext.commands import Cog

from datetime import datetime

from ..db import db

class stats(Cog):
    def __init__(self,bot) -> None:
        super().__init__()
        self.bot = bot

        @Cog.listener
        async def on_message(self,message):
            if not message.author.bot:
                if message.guild:
                    year = str(datetime.now().strftime("%Y"))
                    stats_add_sent_message(message.author)
                    if message.content.startswith('/play'): #Music played
                        db.execute("""UPDATE users_stats SET music_played = users_stats.music_played + 1 WHERE userid=%s""",str(message.author.id))

                    if message.mentions: #mentioned someone
                        for user in message.mentions:
                            if not user.bot:
                                stats_add_mention(message.author,user)

                    if 'quoi' in message.content.lower():
                        stats_add_feur(message.author)
                        

def setup(bot):
    bot.add_cog(stats(bot))


def stats_add_feur(user):      #Nombre de fois ou le bot a repondu 'feur'
    year = str(datetime.now().strftime("%Y"))
    db.execute("""UPDATE users_stats SET feur = users_stats.feur + 1 WHERE userid=%s and year=%s""",str(user.id),year)

def stats_add_mention(user,mention):    #Nombre de mentions individuelles
    year = str(datetime.now().strftime("%Y"))
    db.execute("""INSERT INTO users_mentions(userid,mentioned_user,year,number_of_mentions)
                VALUES(%s,%s,%s,%s)
                ON CONFLICT(userid,mentioned_user,year)
                DO UPDATE SET number_of_mentions = users_mentions.number_of_mentions + 1;""",str(user.id),str(mention.id),year,1)

def stats_add_sent_message(user):  #Nombre de messages envoyés
    year = str(datetime.now().strftime("%Y"))
    db.execute("""INSERT INTO users_stats(userid,year,message_sent)
                VALUES(%s,%s,%s)
                ON CONFLICT(userid,year)
                DO UPDATE SET message_sent = users_stats.message_sent + 1;""",str(user.id),year,1)

def stats_add_music_played(user):   #Nombre de musiques jouées
    db.execute("""UPDATE users_stats SET music_played = users_stats.music_played + 1 WHERE userid=%s""",str(user.id))

