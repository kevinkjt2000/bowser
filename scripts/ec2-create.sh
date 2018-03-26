#!/bin/bash
docker-machine create \
  --driver=amazonec2 \
  --amazonec2-ami=ami-3f061b45 \
  --amazonec2-device-name=/dev/xvda \
  --amazonec2-ssh-user=core \
  bowser

scripts/ec2-update.sh
