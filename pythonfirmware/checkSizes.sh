#!/bin/bash
appSize=$(ls -l ./remote-firmware.bin  | awk  '{print $5}')
otaHex=280000

echo "Application Size     $appSize"

otaDec=$((16#$otaHex))
echo "Flash Partition Size $otaDec"
echo "Available            $(bc <<< "scale=2; ${otaDec}-${appSize}")"
percentage=$(bc <<< "scale=2; ${appSize}*100/${otaDec}")
echo "Used $percentage %"
