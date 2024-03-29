curdir=$(pwd)
echo ${curdir}
echo =====================
export MICROPYTHON_DIR=${curdir}/../../../environments/micropython-custom
export ESPIDF=${curdir}/../../../environments/esp32/espidf5_0
. ${ESPIDF}/export.sh

export BOARD=ESP32_GENERIC
export BOARD_VARIANT=OTA

# export BOARD_DIR=${curdir}/boards/CUSTOM
export FLASH_SIZE=4MB
export PORT=$(ls -1 /dev/tty.usbserial-* | head -n1)
#export PORT=/dev/cu.SLAB_USBtoUART
# export PORT=/dev/tty.usbserial-AD0KDXKW
export FROZEN_MANIFEST=${curdir}/frozenmanifest.py
export PROJECT_DIR=$curdir
# enable for C-USer_Modules
export USER_C_MODULES=$curdir/csrc/micropython.cmake
