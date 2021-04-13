import discord
from discord.ext import commands

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # send message if someone enters voice chat
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        msg_channel_id = 600755633557602310
        message_channel=self.bot.get_channel(msg_channel_id)
        # if the member was not in any voice channel before but is now
        if before.channel is None and after.channel is not None:
            member_ids = after.channel.voice_states.keys()
            # if the channel this member is in only has 1 member - send notification only for the first person that joins
            if len(member_ids) == 1:
                await message_channel.send("IT'S GAMER TIME @GAYMERS")