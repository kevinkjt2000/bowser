#!/bin/bash
mkdir -p backup/redis-data
docker-machine scp bowser:./redis-data/* backup/redis-data/
docker-machine scp bowser:./token.txt backup/
