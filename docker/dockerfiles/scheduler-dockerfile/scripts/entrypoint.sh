#!/bin/bash

# Cron execution format '*/15 * * * *'
S_TIME=$1

# Start the run once job.
echo "Docker container has been started."

# Setup a cron schedule
if [ "$S_TIME" != "" ]; then
    echo "$S_TIME /synchronizator.sh >> /var/log/cron.log 2>&1" > synchronizator.txt
else
    # Default: every day at 00:00
    echo "0 0 * * * /synchronizator.sh >> /var/log/cron.log 2>&1" > synchronizator.txt
fi

echo "# This extra line makes it a valid cron job" >> synchronizator.txt

crontab synchronizator.txt
cron -f