#!/bin/bash

# Check if ./fluentd.conf exists in the current directory
if [ -f "./fluentd.conf" ]; then
    # Check if /etc/fluent/fluentd.conf exists
    if [ ! -f "/etc/fluent/fluentd.conf" ]; then
        echo "/etc/fluent/fluentd.conf does not exist. Creating default configuration file..."

        # Create the fluentd.conf with default configuration
        sudo mkdir -p /etc/fluent
        cat <<EOL | sudo tee /etc/fluent/fluentd.conf > /dev/null
# Fluentd Configuration
<source>
  @type tcp
  port 24224
  bind 0.0.0.0
  tag fluentd.test
</source>

<match fluentd.test>
  @type elasticsearch
  host localhost
  port 9200
  logstash_format true
  index_name fluentd-test
</match>
EOL

        echo "Default fluentd.conf created at /etc/fluent/fluentd.conf."
    fi

    # Replace the existing /etc/fluent/fluentd.conf with ./fluentd.conf
    sudo cp ./fluentd.conf /etc/fluent/fluentd.conf
    echo "Configuration file replaced successfully."

    # Restart Fluentd service
    sudo systemctl restart fluentd.service
    echo "Fluentd restarting"
else
    echo "No fluentd.conf found in the current directory."
fi
