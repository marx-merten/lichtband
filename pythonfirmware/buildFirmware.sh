curdir=$(pwd)
find . -name "__pycache__" -type d -prune -exec rm -rf '{}' '+'


pushd $HOME/projekteHome/marxworld/electronics/environments/micropython/ports/esp32
export ESPIDF=/Users/stefan/projekteHome/marxworld/electronics/environments/esp32/espidf3
. /Users/stefan/projekteHome/marxworld/electronics/environments/esp32/espidf3/export.sh
export BOARD=GENERIC
export FLASH_SIZE=4MB
#export PORT=$(ls -1 /dev/tty.usbserial-*|head -n1)
export PORT=/dev/cu.SLAB_USBtoUART
# export PORT=/dev/tty.usbserial-AD0KDXKW
export PART_SRC=${curdir}/partitions.csv
export FROZEN_MANIFEST=${curdir}/frozenmanifest.py
export PROJECT_DIR=$curdir

echo "building"
make -j8 $*
cp ./build-${BOARD}/firmware.bin ${curdir}/remote-firmware.bin
popd
./checkSizes.sh
