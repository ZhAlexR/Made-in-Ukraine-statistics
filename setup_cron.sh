#!/bin/bash

echo "*/10 * * * * /usr/local/bin/python3 /app/data_parser/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/data-parser-cron

chmod 0644 /etc/cron.d/data-parser-cron

crontab /etc/cron.d/data-parser-cron

cron
