#!/bin/bash
. ./environment.sh >>/dev/null

echo "Choosen $PORT"
rshell -p ${PORT} $*