#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    tag='latest'
  else
    tag=$1
fi

git pull
docker build --no-cache -t weixingp/fyp:"$tag" .