import discord
from discord.ext import commands
import datetime

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # send message if someone enters voice chat
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        msg_channel_id = 600755633557602310
        message_channel=self.bot.get_channel(msg_channel_id)
        if member.bot:
            return
        # if the member was not in any voice channel before but is now
        if before.channel is None and after.channel is not None:
            for guild in self.bot.guilds:
                channels = [c for c in guild.voice_channels]
                total_len = 0
                for c in channels:
                    member_ids = c.voice_states.keys()
                    total_len = total_len + len(member_ids)
                    # ignore bots
                    for m in member_ids:
                        if self.bot.get_user(m).bot:
                            total_len = total_len - 1
                # if only 1 member in all voice channels - send notification only for the first person that joins
                if total_len == 1:
                    # don't spam
                    time_difference = (datetime.datetime.utcnow() - self.bot.last_timeStamp_vc).total_seconds()
                    if time_difference < 900:
                        return
                    else:
                        self.bot.last_timeStamp_vc = datetime.datetime.utcnow()
                        await message_channel.send("IT'S GAMER TIME <@&831364494013497354>")