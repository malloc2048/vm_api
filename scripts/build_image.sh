#!/usr/bin/env bash

if [[ -z "$(docker network ls -f name=api_default)" ]]; then
  docker network create api_default
fi

docker image build . -t elegant_waterfall:latest
