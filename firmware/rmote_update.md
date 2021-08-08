╰─ I  ./buildFirmware.sh &&
curl  --data-binary @remote-application.bin -o /tmp/ota.log  http://172.17.100.43/kernel/ota/upload &&
curl  -H "X-OTA-CHECKSUM: $(sha256sum remote-application.bin|awk '{print $1}')" http://172.17.100.43/kernel/ota/activate
| jq .