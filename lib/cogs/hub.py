import discord
from discord.ext import commands
from wonderwords import RandomWord, Defaults

from ..bot import config

class Hub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.load_config()
        self.created_vc=[]
        self.category = None
        self.hub_vc = None


    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel_deleted):
      for channel in self.created_vc:
          if channel_deleted==channel:
              self.created_vc.remove(channel)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        for channel in self.created_vc:
            if channel==before.channel:
                if not len(before.channel.members):
                    try:
                        await channel.delete()
                    except:
                        pass

        if after.channel is not None:
            if after.channel == self.hub_vc:
                r = RandomWord()
                vc_name = (f"{r.word(include_parts_of_speech=['adjectives'],).title()} {r.word(include_parts_of_speech=['nouns']).title()}")
                new_vc=await self.category.create_voice_channel(vc_name)
                self.created_vc.append(new_vc)
                await member.move_to(new_vc)

    @commands.Cog.listener()
    async def on_ready(self):
            self.category = self.bot.get_channel(int(self.cfg["hub_category_id"]))
            self.hub_vc = self.bot.get_channel(int(self.cfg["hub_vc_id"]))

def setup(bot):
    bot.add_cog(Hub(bot))
