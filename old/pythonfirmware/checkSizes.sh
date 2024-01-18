#!/bin/bash

. ./environment.sh >/dev/null
echo $PART_SRC

appSize=$(ls -l ./remote-application.bin  | awk  '{print $5}')

otaHex=$(grep app ${PART_SRC} | head -n 1 | awk -F , '{print $5}' | awk -F x '{ print $2}')

echo "Application Size     $appSize"

otaDec=$((16#$otaHex))
echo "Flash Partition Size $otaDec"
echo "Available            $(bc <<< "scale=2; ${otaDec}-${appSize}")"
percentage=$(bc <<< "scale=2; ${appSize}*100/${otaDec}")
echo "Used $percentage %"
