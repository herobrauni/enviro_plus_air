#!/bin/bash

mkdir -p /data/sensor
# As we've now updated, copy the current version here so it matches on next pass
# cp /usr/src/app/version /data/sensor/version

echo "================ Starting Balena Sense ================"

exec python /usr/src/app/sensor.py
