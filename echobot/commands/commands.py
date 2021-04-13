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

    @commands.command(name='add_role', help='Add role to user')
    async def add_role(self, context, role:discord.Role, member:discord.Member):
        if role in member.roles:
            await context.channel.send("{0} already has {1} role".format(member.name, role.name))
        else:
            await member.add_roles(role)
            await context.channel.send("{0} role given to {1}".format(role.name, member.name))

    @commands.command(name='remove_role', help='Remove role from user')
    async def remove_role(self, context, role:discord.Role, member:discord.Member):
        if role in member.roles:
            await member.remove_roles(role)
            await context.channel.send("{0} role removed from {1}".format(role.name, member.name))
        else:
            await context.channel.send("{0} does not have {1} role".format(member.name, role.name))