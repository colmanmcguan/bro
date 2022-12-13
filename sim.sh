#!/bin/bash

DEFENDED=./defended
B=$(seq -f "b%g" 1 2)
STATS=$(seq -f "b%gstats" 1 2)
TB=$(seq -f "tb%g" 1 3)
TP=$(seq -f "tp%g" 1 12)

if [ $# -ne 0 ]; then
  for ARG in "$@"; do
    case $ARG in
      "b")
        for CONFIG in $B; do
          python3 ./util/bro.py $CONFIG
        done
        ;;
      "stats")
        for CONFIG in $STATS; do
          python3 ./util/bro.py $CONFIG
        done
	;;
      "tb")
        for CONFIG in $TB; do
          python3 ./util/bro.py $CONFIG
        done
        ;;
      "tp")
        for CONFIG in $TP; do
          python3 ./util/bro.py $CONFIG
        done
        ;;
      *)
        python3 ./util/bro.py $ARG
        ;;
    esac
  done
else
  for CONFIG in $B $STATS $TB $TP; do
    python3 ./util/bro.py $CONFIG
  done
fi
