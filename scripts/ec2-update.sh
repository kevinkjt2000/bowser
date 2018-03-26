#!/bin/bash
tox -r -e package

docker-machine scp dist/bowser.pex bowser:.
docker-machine scp servers.json bowser:.
docker-machine scp token.txt bowser:.

eval $(docker-machine env bowser)
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml up -d
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml restart
