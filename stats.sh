#!/bin/bash

STATS=$(seq -f "b%gstats" 1 2)

if [ $# -ne 0 ]; then
  for ARG in "$@"; do
    case $ARG in
      "tmstmps")
        for CONFIG in $STATS; do
          if [ -d ./defended/$CONFIG ]; then
            python3 ./util/tmstmps.py $CONFIG
          fi
        done
        ;;
      "cluster")
        for CONFIG in $STATS; do
          if [ -d ./defended/$CONFIG ]; then
            python3 ./util/cluster.py $CONFIG
          fi
        done
        ;;
      *)
        if [ -d ./defended/$CONFIG ]; then
          python3 ./util/tmstmps.py $CONFIG 
          python3 ./util/cluster.py $CONFIG
        fi
        ;;
    esac
  done
else
  for CONFIG in $STATS; do
    if [ -d ./defended/$CONFIG ]; then
      python3 ./util/tmstmps.py $CONFIG
      python3 ./util/cluster.py $CONFIG
    fi
  done
  
