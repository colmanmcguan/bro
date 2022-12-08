#!/bin/bash

LOG="./log/undefended"
DEFENDED="./defended"

B=$(seq -f "b%g" 1 2)
TB=$(seq -f "tb%g" 1 3)
TP=$(seq -f "tp%g" 1 12)

if [ $# -ne 0 ]; then
    for ARG in "$@"; do
        case $ARG in
            "b")
                for CONFIG in $B; do
                    python3 ./util/mkdfds.py $DEFENDED/$CONFIG
                done
                ;;
            "tb")
                for CONFIG in $TB; do
                    python3 ./util.mkdfds.py $DEFENDED/$CONFIG
                done
                ;;
            "tp")
                for CONFIG in $TP; do
                    python3 ./util.mkdfds.py $DEFENDED/$CONFIG
                done
                ;;
            *)
                python3 ./util/mkdfds.py $ARG
                ;;
        esac
    done
else
    if [ -d $LOG ]; then
        python3 ./util/mkdfds.py $LOG
    fi
    for CONFIG in $DEFENDED/*; do
        if [ -d $CONFIG ]; then
            python3 ./util/mkdfds.py $CONFIG
        fi
    done
fi
