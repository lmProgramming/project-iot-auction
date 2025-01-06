#!/bin/bash

pip install paho-mqtt

cd ./raspberry-pi/lab11

export DISPLAY=:0.0

sudo bash -c 'echo "allow_anonymous true" >> /etc/mosquitto/mosquitto.conf'
sudo bash -c 'echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf'

sudo apt update

sudo apt install -y mosquitto mosquitto-clients

sudo systemctl start mosquitto.service

python3 ./create_database.py