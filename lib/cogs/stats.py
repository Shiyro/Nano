import discord
from discord.ext.commands import Cog
from discord.commands import message_command

from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from ..db import db

bot = None
class stats(Cog):
    def __init__(self,bot) -> None:
        super().__init__()
        self.bot = bot

    @Cog.listener()
    async def on_message(self,message):
        if not message.author.bot:
            if message.guild:
                year = str(datetime.now().strftime("%Y"))
                stats_add_sent_message(message.author)
                if message.mentions: #mentioned someone
                    for user in message.mentions:
                        if not user.bot:
                            stats_add_mention(message.author,user)
                if 'quoi' in message.content.lower():
                    stats_add_feur(message.author)
        
    @message_command(name="Dit au revoir !",guild_ids=[665676159421251587])
    async def aurevoir(self,ctx,message):
        year = str(datetime.now().strftime("%Y"))
        fanette = self.bot.get_user(249970729418752000)
        db.execute("""INSERT INTO guild_stats(guildid,year,no_goodbye_fanette) VALUES(%s,%s,%s) ON CONFLICT(guildid,year) DO UPDATE SET no_goodbye_fanette = guild_stats.no_goodbye_fanette + 1;""",str(ctx.guild.id),year,1)          
        await ctx.respond(f'{fanette.mention} n\'a pas dis au revoir ? Très bien, nous allons lui niquer sa mère.')

    def stats_add_time_spent_voicechat(self):
        membres = self.bot.get_guild(665676159421251587).members
        year = str(datetime.now().strftime("%Y"))
        for member in membres:
            if not member.bot:
                if member.voice is not None and member.voice.channel is not None:
                    db.execute("""INSERT INTO users_stats(userid,year,voice_channel_time)
                                    VALUES(%s,%s,%s)
                                    ON CONFLICT(userid,year)
                                    DO UPDATE SET voice_channel_time = users_stats.voice_channel_time + 1;""",str(member.id),year,1)

def setup(bot):
    cog = stats(bot)
    bot.add_cog(cog)
    bot.scheduler.add_job(cog.stats_add_time_spent_voicechat, CronTrigger(second=55))


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
    year = str(datetime.now().strftime("%Y"))
    db.execute("""UPDATE users_stats SET music_played = users_stats.music_played + 1 WHERE userid=%s AND year=%s""",str(user.id),year)

def stats_add_aurevoir():   #Nombre de fois ou fanette dit pas au revoir
    year = str(datetime.now().strftime("%Y"))
    pass