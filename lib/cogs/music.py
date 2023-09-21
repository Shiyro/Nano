from discord.ext import commands
import discord
from discord import Activity, ActivityType
from discord.commands import slash_command,message_command
from discord.ui import Button, View

import asyncio
from discord.utils import V
import yt_dlp
from typing import Optional
import logging
import math
from urllib import request
import yt_dlp as ytdl

from . import stats

ydl_opts = {
    "default_search": "auto",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": True,
    "skip_download": True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '256',
    }],
}

# TODO: abstract FFMPEG options into their own file?
FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
"""
Command line options to pass to `ffmpeg` before the `-i`.

See https://stackoverflow.com/questions/43218292/youtubedl-read-error-with-discord-py/44490434#44490434 for more information.
Also, https://ffmpeg.org/ffmpeg-protocols.html for command line option reference.
"""


async def audio_playing(ctx):
    """Verifie que le bot est en train de lire une vidéo."""
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    else:
        return False


async def in_voice_channel(ctx):
    """Verifie que le bot soit dans un channel."""
    voice = ctx.user.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        return False

class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in url_or_search or "youtu.be" in url_or_search:
                video = self._get_info(url_or_search)
            else:
                video =  self._get_info(f"ytsearch:{url_or_search}")
            
            self.stream_url = video["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video[
                "thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for the first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Ajouté par {self.requested_by.name}",
            icon_url=self.requested_by.avatar)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed
    
class MusicInteraction(View):
    def __init__(self,music_player, url):
        super().__init__(timeout=None)
        self.player = music_player
        self.playing = True
        self.video_url = url
        self.add_item(Button(label="Voir sur Youtube",url=url,row=1))

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.grey)
    async def pause_button_callback(self,button,interaction):
        if self.playing:
            button.label = "Play"
            button.style = discord.ButtonStyle.primary
        else:
            button.label = "Pause"
            button.style = discord.ButtonStyle.grey
        self.playing = not self.playing
        await interaction.response.edit_message(view=self)
        self.player._pause_audio(interaction.guild.voice_client)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.grey)
    async def skip_button_callback(self,button,interaction):
        if await audio_playing(interaction) and await in_voice_channel(interaction):
            await self.player._skip(interaction)
            await interaction.response.defer()
        else:
            if not await audio_playing(interaction):
                await interaction.response.send_message("Il n'y a pas de musique en cours.",ephemeral=True)
            elif not in_voice_channel(interaction):
                await interaction.response.send_message("Tu doit être dans le salon avec le bot.",ephemeral=True)

    @discord.ui.button(label="Loop", style=discord.ButtonStyle.grey)
    async def loop_button_callback(self,button,interaction):
        if await self.player._loop(interaction):
            if await self.player.get_loop_status(interaction):
                button.style=discord.ButtonStyle.success
            else:
                button.style=discord.ButtonStyle.grey
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("Il n'y a pas de musique en cours.")

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button_callback(self,button,interaction):
        await self.player._stop(interaction)
        await interaction.response.defer()

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.states = {}

    def get_state(self, guild):
        """Recupere l'etat de la `guild`, ou le créer."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    async def _stop(self, interaction):
        """Quitte le salon vocal."""
        client = interaction.guild.voice_client
        state = self.get_state(interaction.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Pas dans un salon vocal.")

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    async def _skip(self, interaction):
        interaction.guild.voice_client.stop()

    def _play_song(self, client, state, song):
        state.now_playing = song
        _activity = Activity(name=f"{song.title}",type=getattr(ActivityType, "listening", ActivityType.playing))
        asyncio.run_coroutine_threadsafe(self.bot.change_presence(activity=_activity),self.bot.loop)
        channel = client.channel
        source = discord.FFmpegOpusAudio(song.stream_url, before_options=FFMPEG_BEFORE_OPTS, bitrate=256)

        def after_playing(err):
            if state.loop_flag and (len(channel.members)>1):
                next_song = state.now_playing
                self._play_song(client, state, next_song)
            elif (len(state.playlist) > 0) and (len(channel.members)>1) :
                next_song = state.playlist.pop(0)
                if state.player_message is not None:
                    asyncio.run_coroutine_threadsafe(state.player_message.edit(view=None),self.bot.loop)
                self._play_song(client, state, next_song)
                asyncio.run_coroutine_threadsafe(self.send_player(next_song,state),self.bot.loop)
            else:
                asyncio.run_coroutine_threadsafe(state.player_message.edit(view=None),self.bot.loop)
                state.now_playing = None
                asyncio.run_coroutine_threadsafe(client.disconnect(),self.bot.loop)
                asyncio.run_coroutine_threadsafe(self.bot.change_presence(activity=None),self.bot.loop)

        client.play(source, after=after_playing)

    async def _loop(self,interaction):
        if await audio_playing(interaction):
            state = self.get_state(interaction.guild)
            state.loop_flag=not state.loop_flag
            return True
        else:
            return False

    async def get_loop_status(self,interaction):
        state = self.get_state(interaction.guild)
        return state.loop_flag

    @message_command(name="Afficher la queue")
    async def queue(self, interaction, message):
        """Affiche la queue."""
        state = self.get_state(interaction.guild)
        await interaction.response.send_message(self._queue_text(state),ephemeral=True)

    def _queue_text(self, state):
        """Retourne le texte pour l'affichage de la queue."""
        queue = state.playlist
        if len(queue) > 0 or state.now_playing is not None:
            message = ['**Queue :**']
            message +=[f'  [P] **{state.now_playing.title}** (Ajouté par **{state.now_playing.requested_by.name}**)']
            message += [
                f"  [{index+1}] **{song.title}** (Ajouté par **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "La file est vide. Ajoute tes sons !"

    @slash_command()
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Joue l'audio de <url> (ou effectue une recherche de <url> et joue le premier résultat)."""

        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state

        

        if client and client.channel:
            await ctx.defer()
            state.webhook = ctx.followup
            try:
                video = Video(url, ctx.author)
            except yt_dlp.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await state.webhook.send("Une erreur est survenue pendant le téléchargement de la musique.",ephemeral=True)
                return
            state.playlist.append(video)
            await state.webhook.send(content=f"**{video.title}** à été ajouté à la queue")
            await state.webhook.send(embed=video.get_embed(),delete_after=5)
            stats.stats_add_music_played(ctx.user)
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                await ctx.defer()
                state.webhook = ctx.followup
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except yt_dlp.DownloadError as e:
                    await state.webhook.send("Une erreur est survenue pendant le téléchargement de la musique.",ephemeral=True)
                    return
                client = await channel.connect()
                state.loop_flag=False #On reset le loop avant
                state.player_message = await state.webhook.send(embed=video.get_embed(),view = MusicInteraction(self,video.video_url))
                self._play_song(client, state, video)
                stats.stats_add_music_played(ctx.user)

                logging.info(f"Now playing '{video.title}'")
            else:
                await ctx.response.send_message("Tu dois être dans un salon vocal pour faire ça.",ephemeral=True)
                raise commands.CommandError("Tu dois être dans un salon vocal pour faire ça.")

    async def send_player(self,video,state):
        state.player_message = await state.webhook.send(embed=video.get_embed(),view = MusicInteraction(self,video.video_url))

def setup(bot):
    bot.add_cog(Music(bot))

class GuildState:
    """Gestion par guild."""

    def __init__(self):
        self.playlist = []
        self.now_playing = None
        self.webhook = None
        self.player_message = None
        self.loop_flag = False

    def is_requester(self, user):
        return self.now_playing.requested_by == user
