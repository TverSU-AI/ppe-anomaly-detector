#!/usr/bin/env bash

image_name=anomaly
container_name=anomaly

if [ -z "$(docker images -q $image_name)" ]; then
    docker build -f Dockerfile -t $image_name ./
fi

docker run --name $container_name \
       --runtime=nvidia -it --shm-size=64g \
       $image_name
