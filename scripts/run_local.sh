#!/usr/bin/env bash

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
ROOT_DIR=$SCRIPT_DIR/..

# set up the dev stuff for the container
ARGS="${ARGS} -v $ROOT_DIR/api:/home/app/api"
ARGS="${ARGS} -v /sys/fs/cgroup:/sys/fs/cgroup:rw"
ARGS="${ARGS} -v /var/run/libvirt:/var/run/libvirt"

if [ -z "$(docker images -q elegant_waterfall:latest)" ]; then
  echo "API image does not exist, building"
  "${SCRIPT_DIR}"/build_image.sh
fi

# set up the network for the container
if [[ -z "$(docker network ls -q -f name=api_default)" ]]; then
  echo "network not created"
  docker network create api_default
fi

# putting double quotes around the ${ARGS} causes failures in creating the container with the env set and directories mapped
# but pycharm is annoying about flagging it as a warning, so disabled because I don't like the annoyance
# shellcheck disable=SC2086
if [[ -z "$1" ]]; then
  docker container run --network host --device /dev/kvm --rm -it ${ARGS} elegant_waterfall:latest
else
  docker container run --privileged --network host --device /dev/kvm --rm -it --entrypoint  $1 ${ARGS} elegant_waterfall:latest
fi
