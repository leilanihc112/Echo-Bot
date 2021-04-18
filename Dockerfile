# Core tag comes fom build script
# Tells which image to use as a base
ARG echobot_core_tag
FROM echobotcore:$echobot_core_tag

ARG DEBIAN_FRONTEND=noninteractive

# Copy over Echo Bot code into container
COPY . /echobot

# Run Echo Bot
WORKDIR /echobot/echobot
CMD python3 ./echo-bot.py

ENV TZ="America/Chicago"
