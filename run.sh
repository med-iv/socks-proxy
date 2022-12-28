#!/bin/bash

case "$1" in
"python")
  python3 server.py
  ;;
"start")
  docker build -t socks4-proxy-server .
  docker run -p 1080:1080 --name socks4-proxy-server -d socks4-proxy-server
  ;;
"stop")
  docker stop socks4-proxy-server
  ;;
"-h" | "--help" | *)
  echo "You have failed to specify what to do correctly."
  echo "Available options:"
  echo '"./run.sh start" for running docker container'
  echo '"./run.sh stop" for stopping docker container'
  echo '"./run.sh python" for straight python running"'
  exit 1
  ;;
esac
