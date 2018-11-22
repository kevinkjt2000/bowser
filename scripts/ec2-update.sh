#!/bin/bash

docker-machine scp dist/bowser.pex bowser:.

eval $(docker-machine env bowser)
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml restart
