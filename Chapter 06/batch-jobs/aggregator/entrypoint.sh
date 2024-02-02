#!/bin/sh -ex

cd /data/

while true; do
    for file in $(ls); do
        echo "Processing $file"
        sleep 1
        cat $file
        rm $file
    done
    sleep 10
done
