#!/bin/sh
for file in '/data/Twitter dataset/'geoTwitter20*; do
    ./src/map.py --input_path="$file" &
done
