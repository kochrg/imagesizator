#!/bin/bash

# Add protection to /public/ folder if build variables exists

HT_USER=$1
HT_PASSWD=$2

if [ "$HT_USER" != "" ] && [ "$HT_PASSWD" != "" ]; then
    echo "Adding security to /public/ folder"
    htpasswd -bc /etc/apache2/.htpasswd $HT_USER $HT_PASSWD
    sed -i '/Options Indexes/,+2 d' /etc/apache2/sites-available/imagesizator.conf
    sed -i '/<Directory \/var\/www\/imagesizator\/public>/a \\tAuthType Basic\n\tAuthName "Restricted Content"\n\tAuthUserFile \/etc\/apache2/.htpasswd\n\tRequire valid-user\n' /etc/apache2/sites-available/imagesizator.conf
fi
