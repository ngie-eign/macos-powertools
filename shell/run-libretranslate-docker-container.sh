#!/bin/sh

LT_LOAD_ONLY="de,en,es,fr,ja"
LT_UPDATE_MODELS="true"

CONTAINER_PORT="5000"
HOST_PORT="5000"

docker run -ti \
    -e "LT_LOAD_ONLY=${LT_LOAD_ONLY}" \
    -e "LT_UPDATE_MODELS=${LT_UPDATE_MODELS}" \
    --rm \
    --publish "${HOST_PORT}:${CONTAINER_PORT}" \
    libretranslate/libretranslate
