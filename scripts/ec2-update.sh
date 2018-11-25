#!/bin/bash

eval $(docker-machine env bowser)
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml build
docker-compose -f docker-compose.yml -f docker-compose.ec2.yml up -d --remove-orphans
