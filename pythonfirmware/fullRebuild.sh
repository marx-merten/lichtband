#!/bin/bash
rm -f .firmware_md5
rm -f .life_md5
./buildFirmware clean
./rebuild.sh $*