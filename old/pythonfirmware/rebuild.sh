#!/bin/bash
./buildFirmware.sh

oldmd5=$(cat .firmware_md5)
newmd5=$(md5sum remote-firmware.bin)
if [[ "$newmd5" != "$oldmd5" ]]; then
    ./buildFirmware.sh deploy
    echo " =========================== SIZES =============================="
    ./checkSizes.sh
    echo " ================================================================"
fi
echo "$newmd5">.firmware_md5

./boardSync.sh
./boardShell.sh repl