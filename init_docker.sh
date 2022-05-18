#!/bin/sh

docker volume create data;
docker build -t detection .;