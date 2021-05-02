import discord
from discord.ext.commands import Bot
import responses.process
import commands.commands
import notifications.notif
import os
import datetime
import asyncio
import random
from logger import logger

class BetterBot(Bot):
	async def process_commands(self, message):
		ctx = await self.get_context(message)
		await self.invoke(ctx)

bot = BetterBot(command_prefix='.', intents=discord.Intents.all())

def define_cogs():
    return {
        'Processor': (responses.process.Processor, 'responses.process'),
		#'Notifications': (notifications.notif.Notifications, 'notifications.notif'),
		'Text': (commands.commands.Text, 'commands.commands'),
    }

_COGS = define_cogs()

@bot.event
async def on_ready():
	#setattr(BetterBot, "allow_birthday", True)
	#setattr(BetterBot, "allow_regex", True)
	setattr(BetterBot, "last_timeStamp_vc", datetime.datetime.utcfromtimestamp(0))
	setattr(BetterBot, "last_timeStamp_regex", datetime.datetime.utcfromtimestamp(0))
	
	for name, cog in _COGS.items():
		bot.add_cog(cog[0](bot))
		
	print('Bot connected as {0}'.format(bot.user))
	print('Bot is living in {0}'.format(bot.guilds))

@bot.event
async def on_command_error(context, error):
	if isinstance(error, discord.ext.commands.CommandNotFound):
		await context.send("That's not a valid command")

# calculate holidays that are not on a fixed date
def holiday(month, day_of_week, amount, year):
	first = datetime.date(year, month, 1).weekday()
	earliest = 7*(amount - 1)+1
	offset = day_of_week - first
	if offset < 0:
		latest = 7*amount
		day = latest + offset + 1
	else:
		day = earliest + offset
	return_date = datetime.datetime.strftime(datetime.date(year, month, day), '%m/%d')
	return_date = return_date + ' 09:00'
	return return_date

july_time = '07/04 09:00'
april_fools_time = '04/01 09:00'
christmas_time = '12/25 09:00'
halloween_time = '10/31 09:00'
november_time = '11/01 09:00'
st_patricks_time = '03/17 09:00'
valentines_time = '02/14 09:00'
four_twenty_time = '04/20 16:20'
midnight_time = "00:00"
prof_pic_change = "00:00 Sunday"
message_channel_id = 499279740935471109
guild_id = 499279740935471105

# send message on holidays
async def time_check():
	await bot.wait_until_ready()
	message_channel=bot.get_channel(message_channel_id)
	while not bot.is_closed():
		now=datetime.datetime.strftime(datetime.datetime.now(), '%m/%d %H:%M')
		now1=datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
		now2=datetime.datetime.strftime(datetime.datetime.now(), "%H:%M %A")
		if now == july_time:
			holiday_message = ''
			try:
				with open('responses/holiday/4th_of_july.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday 4th of July: Now={0}'.format(now))
			time=90
		elif now == april_fools_time:
			holiday_message = ''
			try:
				with open('responses/holiday/april_fools.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday April Fools: Now={0}'.format(now))
			time=90
		elif now == christmas_time:
			holiday_message = ''
			try:
				with open('responses/holiday/christmas.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday Christmas: Now={0}'.format(now))
			time=90
		elif now == halloween_time:
			holiday_message = ''
			try:
				with open('responses/holiday/halloween.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday Halloween: Now={0}'.format(now))
			time=90
		elif now == november_time:
			holiday_message = ''
			try:
				with open('responses/holiday/november.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday November: Now={0}'.format(now))
			time=90
		elif now == holiday(2, 0, 3, datetime.datetime.now().year):
			holiday_message = ''
			try:
				with open('responses/holiday/presidents_day.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday Presidents Day: Now={0}'.format(now))
			time=90
		elif now == st_patricks_time:
			holiday_message = ''
			try:
				with open('responses/holiday/st_patricks.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday St Patricks: Now={0}'.format(now))
			time=90
		elif now == holiday(11, 3, 4, datetime.datetime.now().year):
			holiday_message = ''
			try:
				with open('responses/holiday/thanksgiving.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday Thanksgiving: Now={0}'.format(now))
			time=90
		elif now == valentines_time:
			holiday_message = ''
			try:
				with open('responses/holiday/valentines.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday Valentines: Now={0}'.format(now))
			time=90
		elif now == four_twenty_time:
			holiday_message = ''
			try:
				with open('responses/holiday/420.txt', 'r', encoding='utf8') as f:
					for line in f:
						holiday_message = holiday_message + bytes([int(x,2) for x in line]).decode('utf-8')
			except:
				print(sys.exc_info()[0])
			f.close()
			await message_channel.send(holiday_message)
			logger.info('Holiday 420: Now={0}'.format(now))
			time=90
		elif now1 == midnight_time:
			#bot.allow_birthday = True
			if now2 == prof_pic_change:
				for guild in bot.guilds:
					if guild.id == guild_id:
						member = random.choice(guild.members)
						while member.name == bot.user.name:
							member = random.choice(guild.members)
						await member.avatar_url.save("pfp/pfp.jpg")
						fp = open("pfp/pfp.jpg", "rb")
						file = fp.read()
						await bot.user.edit(avatar=file)
						mem_nick = member.display_name
						await guild.me.edit(nick=mem_nick)
						logger.info('Profile Pic & Nickname: Now={0}, member.display_name={1}'.format(now, member.display_name))
			time=900
		else:
			time=1
		await(asyncio.sleep(time))

bot.loop.create_task(time_check())

bot.run(open("secrets.txt","r").read())