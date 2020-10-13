#!/bin/bash

mkdir -p /data/sensor
# As we've now updated, copy the current version here so it matches on next pass
cp /usr/src/app/version /data/sensor/version

touch /data/sensor/bsec_iaq.state
cp -n /usr/src/app/bsec_bme680_linux/bsec_iaq.config /data/sensor/bsec_iaq.config

echo "================ Starting Balena Sense ================"

exec python /usr/src/app/scripts/sensor.py
