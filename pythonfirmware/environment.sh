curdir=$(pwd)

# =====
# Environment - choose idf version and micropython repository here
# =====

export MICROPYTHON_DIR=${curdir}/../../../environments/micropython-master
export ESPIDF=${curdir}/../../../environments/esp32/espidf4
export IDF_PATH=${ESPIDF}
. ${ESPIDF}/export.sh

# Board generics
# =====
export BOARD=GENERIC_MARXWORLD
export BOARD_DIR=${curdir}/boards/CUSTOM
export FLASH_SIZE=4MB
export PART_SRC=${curdir}/partitions-ota.csv

# Serial port communication
# =====

#export PORT=$(ls -1 /dev/tty.usbserial-*|head -n1)
export PORT=/dev/cu.SLAB_USBtoUART
# export PORT=/dev/tty.usbserial-AD0KDXKW

# Basics
# =====
export FROZEN_MANIFEST=${curdir}/frozenmanifest.py
export PROJECT_DIR=$curdir
export USER_C_MODULES=$curdir/csrc/modules/
