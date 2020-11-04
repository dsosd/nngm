#!/bin/bash

FILE=$(echo -n "$1" | sed "s#$(pwd)/##g")
MODE="$2"

FILE_KEY=$(echo -n "$FILE" | sed -r "s#.*?\.dir/##g")
OUT_FILE="curr_hashes"

HASH=$(sha256sum "$FILE" | sed -r "s/([0-9a-f]+).*/\1/g")

if [[ "$MODE" = "enforcing" ]]; then
	echo "!$FILE_KEY: $HASH" >>"$OUT_FILE"
elif [[ "$MODE" = "bootstrap" ]]; then
	echo "$FILE_KEY: $HASH" >>"$OUT_FILE"
elif [[ "$MODE" = "permissive" ]]; then
	echo "?$FILE_KEY: $HASH" >>"$OUT_FILE"
else
	echo "ERROR" >>"$OUT_FILE"
fi
