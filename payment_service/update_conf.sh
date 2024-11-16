#!/bin/bash
if [ -f "./fluentd.conf" ]; then
    sudo cp ./fluentd.conf /etc/fluent/fluentd.conf
    echo "Configuration file replaced successfully."
    sudo systemctl restart fluentd.service
    echo "fluentd restarting"
else
    echo "No conf file found."
fi
