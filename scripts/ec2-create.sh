#!/bin/bash
docker-machine create \
  --driver=amazonec2 \
  --amazonec2-ami=ami-03ed1c12a1dd84320 \
  --amazonec2-device-name=/dev/xvda \
  --amazonec2-ssh-user=core \
  bowser

scripts/ec2-update.sh
