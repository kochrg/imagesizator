# syntax=docker/dockerfile:1

FROM ubuntu:21.04
ARG S_TIME
ENV S_TIME=${S_TIME}

RUN apt update 
RUN apt upgrade -y
# Install nano for edition
RUN apt install nano
# Install cron
RUN apt -y install cron
# Install wget
RUN apt -y install wget
# Copy code and install requirements
# --- ADDING CRON JOBS ---
# Add files
COPY ./docker/dockerfiles/scheduler-dockerfile/scripts/synchronizator.sh /synchronizator.sh
COPY ./docker/dockerfiles/scheduler-dockerfile/scripts/entrypoint.sh /entrypoint.sh 
RUN chmod +x /entrypoint.sh /synchronizator.sh
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Add the scripts to cron
ENTRYPOINT /entrypoint.sh "${S_TIME}"