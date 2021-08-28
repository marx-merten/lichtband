#!/bin/bash
. ./environment.sh >>/dev/null


oldmd5=$(cat .web_md5)
newmd5=$(find ../adminweb/build -type f -exec md5sum '{}' ';' | md5sum | awk '{print$1}')
if [[ "$newmd5" != "$oldmd5" ]]; then
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
${DIR}/boardShell.sh rsync -m  $DIR/../adminweb/build /pyboard/html
fi
echo "$newmd5">.web_md5
