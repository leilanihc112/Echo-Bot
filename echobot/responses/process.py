import discord
from discord.ext import commands
import re
import sys
import os
import random
import datetime

# Process regexes and send response
class Processor(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.regexes = {}
		try:
			with open('responses/regex_items.txt') as f:
				for line in f:
					regex, response, emoji = line.strip().split('\t', 2)
					regex1 = regex.split(' ')
					response1 = response.split(' ')
					emoji1 = emoji.split(' ')
					regex2 = bytes([int(x,2) for x in regex1]).decode('utf-8')
					response2 = bytes([int(x,2) for x in response1]).decode('utf-8')
					emoji2 = bytes([int(x,2) for x in emoji1]).decode('utf-8')
					# response is a folder in responses/regex folder
					self.regexes[regex2] = [response2.strip(), emoji2.strip()]
		except:
			print(sys.exc_info()[0])
			raise
		f.close()
		try:
			for reg, resp in self.regexes.items():
				if not (os.path.isdir(os.getcwd() + '/responses/regex' + '/' + resp[0])):
					print(resp[0] + ' regex folder does not exist')
		except:
			print(sys.exc_info()[0])
			raise

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return
		if message.content.startswith(self.bot.command_prefix):
			return
		for reg, resp in self.regexes.items():
			try:
				if re.search(reg, message.content, re.IGNORECASE):
					# react with emoji
					for guild in self.bot.guilds:
						for emoji in guild.emojis:
							if emoji.name == resp[1]:
								await message.add_reaction(emoji)
					if self.bot.allow_regex == True:
						# don't spam
						time_difference = (datetime.datetime.utcnow() - self.bot.last_timeStamp_regex).total_seconds()
						if time_difference < 3:
							return
						else:
							self.bot.last_timeStamp_regex = datetime.datetime.utcnow()
							# limit probability on which this is triggered
							if random.random() < 0.4:
								try:
									response_file = random.choice(os.listdir(os.getcwd() + '/responses/regex' + '/' + resp[0]))
									response_message = ''
									with open('responses/regex/' + '/' + resp[0] + '/' + response_file, 'r') as f:
										for line in f:
											temp_line = line.split(' ')
											response_message = response_message + bytes([int(x,2) for x in temp_line]).decode('utf-8')
									response_message.replace('\\n', '\n')
								except:
									print(sys.exc_info()[0])
								f.close()
								await message.channel.send(response_message)
			except KeyError as e:
				print(e)
				continue
			if self.bot.allow_birthday:
				if re.search('happy birthday|happy bday|hbd', message.content, re.IGNORECASE):
					try:
						response_message = ''
						with open('responses/regex/birthday/birthday.txt', 'r') as f:
							for line in f:
								temp_line = line.split(' ')
								response_message = response_message + bytes([int(x,2) for x in temp_line]).decode('utf-8')
							response_message.replace('\\n', '\n')
					except:
						print(sys.exc_info()[0])
					f.close()
					self.bot.allow_birthday = False
					await message.channel.send(response_message)