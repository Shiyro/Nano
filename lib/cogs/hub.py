import discord
from discord.ext import commands
from wonderwords import RandomWord, Defaults

import os

class Hub(commands.Cog):

    def __init__(self, bot:discord.Bot):
        self.bot = bot
        self.created_vc=[]
        self.CATEGORY_ID = os.getenv('HUB_VOICE_ID')
        self.HUB_ID = os.getenv('HUB_CREATE_CATEGORY')
        self.RANDOM = RandomWord()

    async def create_new_channel(self):
        new_vc=await self.get_category().create_voice_channel(name=self.get_random_word())
        self.created_vc.append(new_vc)
        return new_vc
    
    def get_category(self) :
        return self.bot.get_channel(int(self.CATEGORY_ID))
    
    def get_random_word(self) -> str :
        return (f"{self.RANDOM.word(include_parts_of_speech=['adjectives'],).title()}\
                  {self.RANDOM.word(include_parts_of_speech=['nouns']).title()}")


    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel_deleted):
      for channel in self.created_vc:
          if channel_deleted==channel:
              self.created_vc.remove(channel)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        if before in self.created_vc:
            if len(before.channel.members) == 0:
                await before.delete()

        if after.channel is None: 
            return
        
        if after.channel == self.bot.get_channel(int(self.HUB_ID)):
            await member.move_to(self.create_new_channel())


    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            pass
            

def setup(bot):
    bot.add_cog(Hub(bot))
