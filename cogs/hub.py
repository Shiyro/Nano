import discord
from discord.ext import commands

class hub(commands.Cog):
    def __init__(self, client,config):
        self.client = client
        self.config = config
        self.created_vc=[]

    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel_deleted):
      for channel in self.created_vc:
          if channel_deleted==channel:
              self.created_vc.remove(channel)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        Category = self.client.get_channel(910433640364781598)
        for channel in self.created_vc:
            if channel==before.channel:
                if not len(before.channel.members):
                    try:
                        await channel.delete()
                    except:
                        pass
        if after.channel is not None:
            if after.channel.id == 910433688578297866:
                new_vc=await Category.create_voice_channel(f"𝓥𝓞𝓒𝓞 - {len(self.created_vc)+1}")
                self.created_vc.append(new_vc)
                await member.move_to(new_vc)
