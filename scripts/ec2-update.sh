#!/bin/bash
make package

docker-machine scp dist/requirements.pex bowser:.
docker-machine scp dist/bowser.pex bowser:.
docker-machine scp token.txt bowser:.

eval $(docker-machine env bowser)
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml restart
