#!/bin/bash

# Cron execution format '* * * * *'
S_TIME=$1

# Start
echo "Docker container has been started."

# Setup a cron schedule
if [ "$S_TIME" != "" ]; then
    echo "$S_TIME /synchronizator.sh >> /var/log/cron.log 2>&1" > synchronizator.txt
else
    # Default: every day at 00:00
    echo "0 0 * * * /synchronizator.sh >> /var/log/cron.log 2>&1" > synchronizator.txt
fi

echo "# Add this extra line for a valid cron job" >> synchronizator.txt

crontab synchronizator.txt
cron -f