import discord
from discord.ext import commands

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_prev_message(self, context, message_limit=25):
        """Search through previous messages until find one that contains text"""
        for message in (await context.channel.history(limit=message_limit).flatten())[1:]:
            if message.content:
                resp = str(message.content)
                return resp
        return ""

    @commands.command(name='echo', help='Display line of text/string passed as argument')
    async def echo(self, context, *, content:str=""):
        if content == "":
            content = await self.get_prev_message(context)
        await context.channel.send(content)

    @commands.command(name='regex', help='Toggle regex responses')
    async def regex(self, context, *, content:str=""):
        if content.lower() == "on":
            if self.bot.allow_regex == True:
                content = "Regex responses already enabled"
            else:
                self.bot.allow_regex = True
                content = "Regex responses enabled"
        elif content.lower() == "off":
            if self.bot.allow_regex == False:
                content = "Regex responses already disabled"
            else:
                self.bot.allow_regex = False
                content = "Regex responses disabled"
        else:
            content = "Invalid arg - must be 'on' or 'off'"
        await context.channel.send(content)