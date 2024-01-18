#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
port=/dev/cu.SLAB_USBtoUART
rshell -l
echo "Choosen $port"
rshell -p ${port} $*