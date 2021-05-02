import discord
from discord.ext import commands
from logger import logger

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='get_log', help='Get log file')
    async def get_log(self, context):
        await context.channel.send(file=discord.File('log/echo-bot-log.log'))

    @get_log.error
    async def get_log_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("GET_LOG ERROR " + str(error))

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

    @echo.error
    async def echo_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("ECHO ERROR " + str(error))

    '''
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

    @regex.error
    async def regex_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("REGEX ERROR " + str(error))
    '''

    @commands.command(name='add_role', help='Add role to user')
    async def add_role(self, context, role:discord.Role, member:discord.Member):
        if role in member.roles:
            await context.channel.send("{0} already has {1} role".format(member.name, role.name))
        else:
            await member.add_roles(role)
            await context.channel.send("{0} role given to {1}".format(role.name, member.name))

    @add_role.error
    async def add_role_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("ADD_ROLE ERROR " + str(error))

    @commands.command(name='remove_role', help='Remove role from user')
    async def remove_role(self, context, role:discord.Role, member:discord.Member):
        if role in member.roles:
            await member.remove_roles(role)
            await context.channel.send("{0} role removed from {1}".format(role.name, member.name))
        else:
            await context.channel.send("{0} does not have {1} role".format(member.name, role.name))

    @remove_role.error
    async def remove_role_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("REMOVE_ROLE ERROR " + str(error))

    @commands.command(name='create_role', help='Create new role')
    async def create_role(self, context, *, name):
        guild = context.guild
        if discord.utils.get(guild.roles, name=name):
            await context.send("Role '{0}' already exists".format(name))
        else:
            await guild.create_role(name=name)
            await context.send("Role '{0}' has been created".format(name))

    @create_role.error
    async def create_role_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("CREATE_ROLE ERROR " + str(error))

    @commands.command(name='delete_role', help='Delete existing role')
    async def delete_role(self, context, *, role: discord.Role):
        guild = context.guild
        if discord.utils.get(guild.roles, name=role.name):
            await role.delete()
            await context.send("Role '{0}' has been deleted".format(role.name))
        else:
            await context.send("Error")

    @delete_role.error
    async def delete_role_error(self, ctx, error):
        await ctx.send("Error. Check log file")
        logger.info("DELETE_ROLE ERROR " + str(error))

    @commands.command(name='join', help='Have Echo join a voice channel')
    async def join(self, context, channel=None):
        if channel == None:
            channel = context.author.voice.channel
        if context.voice_client is None:
            await channel.connect()
        else:
            await context.voice_client.move_to(channel)

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            logger.info("JOIN ERROR " + str(error))
            msg = 'You must be connected to a voice channel before invoking this command'
            await ctx.send(msg)
        else:
            await ctx.send("Error. Check log file")
            logger.info("JOIN ERROR " + str(error))

    @commands.command(name='leave', help='Have Echo leave a voice channel')
    async def leave(self, context):
        await context.voice_client.disconnect()

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            logger.info("LEAVE ERROR " + str(error))
            msg = 'Not currently connected to a voice channel'
            await ctx.send(msg)
        else:
            await ctx.send("Error. Check log file")
            logger.info("LEAVE ERROR " + str(error))

    @commands.command(name='echo_reset', help='Reset avatar and nickname')
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def echo_reset(self, context):
        fp = open("pfp/echo_pfp.jpg", "rb")
        file = fp.read()
        await self.bot.user.edit(avatar=file)
        guild = context.guild
        await guild.me.edit(nick="Echo")
        await context.send("Successfully reset nickname and profile pic")

    @echo_reset.error
    async def echo_reset_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            logger.info("ECHO_RESET ERROR " + str(error))
            msg = 'This command is rate limited, please try again in {:.0f}s'.format(error.retry_after)
            await ctx.send(msg)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Error. Check log file")
            logger.info("ECHO_RESET ERROR " + str(error))
        else:
            await ctx.send("Error. Check log file")
            logger.info("ECHO_RESET ERROR " + str(error))