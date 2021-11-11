from discord.ext import commands
import discord
import asyncio
import youtube_dl
from typing import Optional
import logging
import math
from urllib import request
from cogs.Musique.video import Video

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
        raise commands.CommandError("Ne joue aucune musique.")


async def in_voice_channel(ctx):
    """Verifie que le bot soit dans un channel."""
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError(
            "Tu dois être dans un salon vocal.")

class Music(commands.Cog):

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config[__name__.split(".")[
            -1]]  # retrieve module name, find config entry
        self.states = {}
        self.bot.add_listener(self.on_reaction_add, "on_reaction_add")

    def get_state(self, guild):
        """Recupere l'etat de la `guild`, ou le créer."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    @commands.command(aliases=["leave"])
    @commands.guild_only()
    async def stop(self, ctx):
        """Quitte le salon vocal."""
        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)
        if client and client.channel:
            await client.disconnect()
            state.playlist = []
            state.now_playing = None
        else:
            raise commands.CommandError("Pas dans un salon vocal.")

    @commands.command(aliases=["resume"])
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def pause(self, ctx):
        """Met la musique en pause ou relance la lecture."""
        client = ctx.guild.voice_client
        self._pause_audio(client)

    def _pause_audio(self, client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    @commands.check(in_voice_channel)
    async def skip(self, ctx, index:Optional[int]):
        """Skip la musique actuelle."""
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client

        if index is not None:
            for i in range(index-1):
                state.playlist.pop(0)
        client.stop()

    def _play_song(self, client, state, song):
        state.now_playing = song
        channel = client.channel
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url, before_options=FFMPEG_BEFORE_OPTS), volume=state.volume)

        def after_playing(err):
            if state.loop_flag and (len(channel.members)>1):
                next_song = state.now_playing
                self._play_song(client, state, next_song)
            elif (len(state.playlist) > 0) and (len(channel.members)>1) :
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                 self.bot.loop)

        client.play(source, after=after_playing)

    @commands.command()
    @commands.guild_only()
    @commands.check(audio_playing)
    async def loop(self, ctx):
        """Repète en boucle la musique actuelle"""
        state = self.get_state(ctx.guild)
        await self._loop_audio(state)
        if state.loop_flag:
            await ctx.send(f"**Loop:** Activé !")
        else:
            await ctx.send(f"**Loop:** Désactivé !")

    async def _loop_audio(self,state):
        state.loop_flag=not state.loop_flag

    @commands.command(aliases=["q", "playlist"])
    @commands.guild_only()
    @commands.check(audio_playing)
    async def queue(self, ctx):
        """Affiche la queue."""
        state = self.get_state(ctx.guild)
        await ctx.send(self._queue_text(state))

    def _queue_text(self, state):
        """Retourne le texte pour l'affichage de la queue."""
        queue = state.playlist
        if len(queue) > 0:
            message = ['**Queue :**']
            message +=[f'  [P] **{state.now_playing.title}** (Ajouté par **{state.now_playing.requested_by.name}**)']
            message += [
                f"  [{index+1}] **{song.title}** (Ajouté par **{song.requested_by.name}**)"
                for (index, song) in enumerate(queue)
            ]  # add individual songs
            return "\n".join(message)
        else:
            return "La queue est vide."

    @commands.command(brief="Vide la queue.")
    @commands.guild_only()
    @commands.check(audio_playing)
    async def clear(self, ctx):
        """Vide la queue."""
        state = self.get_state(ctx.guild)
        state.playlist = []

    @commands.command(brief="Joue une vidéo depuis <url>.")
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""

        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)  # get the guild's state

        if client and client.channel:
            try:
                video = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                logging.warn(f"Error downloading video: {e}")
                await ctx.send(
                    "Une erreur est survenue pendant le téléchargement de la musique.")
                return
            state.playlist.append(video)
            message = await ctx.send(
                "Ajouté à la queue.", embed=video.get_embed())
            await self._add_reaction_controls(message)
        else:
            if ctx.author.voice is not None and ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    video = Video(url, ctx.author)
                except youtube_dl.DownloadError as e:
                    await ctx.send(
                        "Une erreur est survenue pendant le téléchargement de la musique.")
                    return
                client = await channel.connect()
                state.loop_flag=False #On reset le loop avant
                self._play_song(client, state, video)
                message = await ctx.send("", embed=video.get_embed())
                await self._add_reaction_controls(message)
                logging.info(f"Now playing '{video.title}'")
            else:
                raise commands.CommandError(
                    "Tu dois être dans un salon vocal pour faire ça.")

    async def on_reaction_add(self, reaction, user):
        """Reponds a l'ajout de reactions"""
        message = reaction.message
        if user != self.bot.user and message.author == self.bot.user:
            await message.remove_reaction(reaction, user)
            if message.guild and message.guild.voice_client:
                user_in_channel = user.voice and user.voice.channel and user.voice.channel == message.guild.voice_client.channel
                permissions = message.channel.permissions_for(user)
                guild = message.guild
                state = self.get_state(guild)
                client = message.guild.voice_client
                if reaction.emoji == "⏯":
                    # pause audio
                    self._pause_audio(client)
                elif reaction.emoji == "⏭":
                    # skip audio
                    client.stop()
                elif reaction.emoji == "⏮":
                    state.playlist.insert(
                        0, state.now_playing
                    )  # insert current song at beginning of playlist
                    client.stop()  # skip ahead
                elif reaction.emoji == "🔁":
                    await self._loop_audio(state)
                    if state.loop_flag:
                        await message.channel.send(f"**Loop:** Activé !")
                    else:
                        await message.channel.send(f"**Loop:** Désactivé !")

    async def _add_reaction_controls(self, message):
        """Ajoute un 'panneau de controle' de reaction au message pour controler le bot."""
        CONTROLS = ["⏮", "⏯", "⏭","🔁"]
        for control in CONTROLS:
            await message.add_reaction(control)


class GuildState:
    """Gestion par guild."""

    def __init__(self):
        self.volume = 1.0
        self.playlist = []
        self.now_playing = None
        self.loop_flag = False

    def is_requester(self, user):
        return self.now_playing.requested_by == user
