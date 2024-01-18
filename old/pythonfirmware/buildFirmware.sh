curdir=$(pwd)
find . -name "__pycache__" -type d -prune -exec rm -rf '{}' '+'

. ./environment.sh

pushd ${MICROPYTHON_DIR}/ports/esp32

echo "building"
make -j8 $*
cp ./build-${BOARD}/firmware.bin ${curdir}/remote-firmware.bin
cp ./build-${BOARD}/application.bin ${curdir}/remote-application.bin

popd
