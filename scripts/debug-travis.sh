#!/usr/bin/env bash

docker run --name travis-debug -dit -v /var/run/docker.sock:/var/run/docker.sock travisci/ci-garnet:packer-1512502276-986baf0 /sbin/init
function stop_travis {
  docker rm -f travis-debug
}
trap stop_travis EXIT

docker exec -it travis-debug bash -l
