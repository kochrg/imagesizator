#!/bin/bash
cd "$(dirname "$0")"

openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out ./server-certificates/server.crt \
            -keyout ./server-certificates/server.key
