#!/bin/bash
# This will hopefully build and run the echo bot docker container
# Also hopefully will skip building if it has already been built
set -euo pipefail

# Ensure that the bot is not already running
docker rm --force echobot >/dev/null 2>&1 || true

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Get tag for echobot-core using commit hash
ECHOBOT_CORE_NAME=echobotcore
ECHOBOT_CORE_TAG=$(git -C "${DIR}" rev-list --abbrev-commit -1 HEAD -- ./echobot-core-docker)

CORE_IMAGE_NAME="${ECHOBOT_CORE_NAME}:${ECHOBOT_CORE_TAG}"

# Image name and tag for main container
IMAGE_NAME=echobot
IMAGE_TAG=$(git -C "${DIR}" rev-parse --short HEAD)

FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

IMAGE_REBUILD=true
# Check various rebuild conditions
if [[ $( git status --porcelain "${DIR}/echobot-core-docker") ]]; then
    # Core dockerfile needs to be rebuilt
    ECHOBOT_CORE_TAG=dirty
    CORE_IMAGE_NAME="${ECHOBOT_CORE_NAME}:${ECHOBOT_CORE_TAG}"
    IMAGE_TAG=dirty
    FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
elif [[ $(git -C "${DIR}" diff --stat) != '' ]]; then
    # Main repo is dirty, but core dockerfile is clean
    IMAGE_TAG=dirty
    FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
elif docker inspect --type=image "${FULL_IMAGE_NAME}" >/dev/null 2>&1; then
    # Neither the core folder or the repo is dirty, and we have an image for this commit
    IMAGE_REBUILD=false
fi

if [[ $IMAGE_REBUILD == true ]]; then
    if ! docker inspect --type=image "${CORE_IMAGE_NAME}" >/dev/null 2>&1 \
      || [[ $ECHOBOT_CORE_TAG == dirty ]]; then
        # Rebuild core image
        docker build -t "${CORE_IMAGE_NAME}" "${DIR}/echobot-core-docker"
    fi
    #Export core tag as some kind of env var?
    docker build --build-arg echobot_core_tag=$ECHOBOT_CORE_TAG -t "${FULL_IMAGE_NAME}" "${DIR}"
fi

# Run image
docker run --detach --name echobot "${FULL_IMAGE_NAME}"