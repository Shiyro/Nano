import discord
from discord.ext import commands
import youtube_dl
import asyncio
import time
from typing import Optional

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())
queue = []
urls = []
loop = False
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': True,
    'quiet': False,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


class musique(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='join', help="Rejoins le salon vocal")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("T'es pas dans un ᘎOᙅO !")
            return False
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            return True
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            return True

    @commands.command(name='play',help="Joue une musique depuis Youtube")
    async def play(self, ctx, url):
        global queue  #Songs queue
        global urls
        if(await self.join(ctx)):  #calls the join command to join the vc
          #async with ctx.typing():
          player = await YTDLSource.from_url(url, loop=self.client.loop)
          if queue:
              queue.append(player)
              urls.append(url)
              await ctx.send(f'**Ajouté à la queue : **{player.title}')
          else:
              queue.append(player)
              urls.append(url)
              await self.start_playing(ctx)

    async def start_playing(self, ctx):
        global queue
        global loop
        global urls
        server = ctx.message.guild
        voice_channel = server.voice_client
        if queue:
            try:
                voice_channel.play(queue[0], after=lambda e: asyncio.run(self.end_playing(ctx)))
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(f'{queue[0].title}')))
                await ctx.send(f'**Lis actuellement : **{queue[0].title}')
            except:
                pass

    async def end_playing(self,ctx):
        global urls
        global queue
        if not loop:
          try:
            del (queue[0])
            del (urls[0])
          except:
            pass
        if queue:
            await self.start_playing(ctx)
        else:
          await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="les étoiles"))

    @commands.command(name='queue', help='Affiche la queue')
    async def queue_(self, ctx):
        global queue
        list_ = '**Queue :**\n'
        for i in range(len(queue)):
          if i==0:
            list_ += (f'[P] {queue[i].title}\n')
          else:
            list_ += (f'[{i}] {queue[i].title}\n')
        await ctx.send(list_)

    @commands.command(name='clear', help='Vide la queue')
    async def clear(self, ctx):
        global queue
        global urls
        try:
            queue.clear()
            urls.clear()
            await ctx.send("La queue à été vidé !")
        except:
            await ctx.send("Une erreur est survenu !")

    '''@commands.command(name='loop', help='loop the current song')
    async def loop_(self, ctx):
        global loop
        loopurl = urls[0]
        if loop == False:
            loop = True
            await ctx.send(f"**Looping : **{queue[0].title}")
        else:
            loop = False
            await ctx.send(f"**Stop looping**")'''

    @commands.command(name='stop', help='Stop la musique')
    async def stop(self,ctx):
        global loop
        loop = False
        queue.clear()
        urls.clear()
        ctx.voice_client.stop()

    @commands.command(name='skip', help='Lis la musique suivante dans la queue, ou celle précisé')
    async def skip(self,ctx,message:Optional[int]):
      if message == None:
        message = 1
      if message>(len(queue)-1):
        await ctx.send(f"**Ooops, hors de porté !**")
      else:
        for i in range(message-1):
          try:
            del(queue[0])
            del(urls[0])
          except:
            pass
        await ctx.send(f"**Lis actuellement : **{queue[1].title}")
        ctx.voice_client.stop()

    @commands.command(name='resume', help='Redémarre la musique')
    async def resume(self,ctx):
      ctx.voice_client.resume()
      await ctx.send(f"**Resumed !**")

    @commands.command(name='pause', help='Met pause à la musique')
    async def pause(self,ctx):
      ctx.voice_client.pause()
      await ctx.send(f"**Paused !**")

def setup(client):
    client.add_cog(musique(client))
