import discord
from discord.ext import commands
import re
import sys
import os
import random
import datetime
from random import randint
from typing import List

def msg_generator(bigramlm) -> List[str]:
    generated_tokens = []
    token = '<s>'
    while len(generated_tokens) < 100:
        token = bigramlm.fd[(token,)]
        # skip <UNK>
        # if '<UNK>' in token:
            # del token['<UNK>']
        # if there are no tokens left, just do end token
        if len(token) == 0:
            token = '</s>'
        elif len(token) >= 8:
            if token != '<s>':
                token = token.most_common(8)
                index = randint(0,7)
            else:
                token = token.most_common(len(token))
                index = randint(0,len(token)-1)
        else:
            token = token.most_common(len(token))
            index = randint(0,len(token)-1)
        token = token[index][0]
        # if we've hit end token, break while loop
        if token == '</s>':
            break
        else:
            generated_tokens.append(token)
    # separate tokens by space, except for punctuation
    if generated_tokens:
        generated_msg = generated_tokens[0]
        for i in range(1, len(generated_tokens)):
            if i == 1:
                if generated_tokens[0] in '.,!?;\(\)\[\]\{\}&':
                    generated_msg += generated_tokens[i]
                else:
                    generated_msg += (" " + generated_tokens[i])
            else:
                if generated_tokens[i] not in '.,!?;\(\)\[\]\{\}&':
                    generated_msg += (" " + generated_tokens[i])
                else:
                    generated_msg += generated_tokens[i]
    else:
        generated_msg = "yeah bro"
    return generated_msg


# Process regexes and send response
class Processor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        '''
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
        '''

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        if message.mention_everyone:
            return
        if self.bot.user.mentioned_in(message):
            msg = msg_generator(self.bot.lm)
            await message.channel.send(msg)
        '''
        for reg, resp in self.regexes.items():
            #try:
            if re.search(reg, message.content, re.IGNORECASE):
                # react with emoji
                for guild in self.bot.guilds:
                    for emoji in guild.emojis:
                        if emoji.name == resp[1]:
                            await message.add_reaction(emoji)
                    if self.bot.allow_regex == True:
                        # don't spam
                        time_difference = (datetime.datetime.utcnow() - self.bot.last_timeStamp_regex).total_seconds()
                        if time_difference < 300:
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
        '''