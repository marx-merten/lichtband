curdir=$(pwd)

export ESPIDF=${curdir}/../../../environments/esp32/espidf3
. ${ESPIDF}/export.sh
export BOARD=GENERIC_OTA
export FLASH_SIZE=4MB
#export PORT=$(ls -1 /dev/tty.usbserial-*|head -n1)
export PORT=/dev/cu.SLAB_USBtoUART
# export PORT=/dev/tty.usbserial-AD0KDXKW
# export PART_SRC=${curdir}/partitions.csv
export PART_SRC=${curdir}/partitions-ota.csv
export FROZEN_MANIFEST=${curdir}/frozenmanifest.py
export PROJECT_DIR=$curdir
