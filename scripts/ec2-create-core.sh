#!/bin/bash
docker-machine create \
  --driver=amazonec2 \
  --amazonec2-ami=ami-3f061b45 \
  --amazonec2-device-name=/dev/xvda \
  --amazonec2-ssh-user=core \
  bowser

docker-machine scp dist/bowser.pex bowser:.
docker-machine scp servers.json bowser:.
docker-machine scp token.txt bowser:.

eval $(docker-machine env bowser)
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml up -d
