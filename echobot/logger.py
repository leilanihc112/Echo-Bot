import logging
from logging import handlers
import os

if not os.path.exists("log/echo-bot-log.log"):
	f = open("log/echo-bot-log.log", "w")
	f.close()
logger = logging.getLogger('echo-bot')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(filename='log/echo-bot-log.log', when='midnight', interval=1, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
handler.suffix = "%Y%m%d"
logger.addHandler(handler)