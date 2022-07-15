#!/bin/bash

HOST_WWW_DATA_GID=$1
CONT_WWW_DATA_GID=$(getent group www-data | cut -d: -f3)

# HOST_USER_GID=$2
# HOST_USER_GNAME=$3

# $(getent group groupname | cut -d: -f3) -> get GID with a given groupname
# $(getent group gid | cut -d: -f1) -> get groupname with a given gid

# Check if www-data group exists and have the same gid than the host
if [ "$CONT_WWW_DATA_GID" != "" ]; then
    # Group www-data exists in container, check if have the same GID
    if [ "$HOST_WWW_DATA_GID" != "$CONT_WWW_DATA_GID" ]; then
        # host www-data GID != container www-data GID, change local GID
        
        # Check if the HOST_WWW_DATA_GID is in use in the container
        if [ "$(getent group $HOST_WWW_DATA_GID | cut -d: -f1)" != "" ]; then
            # GID in use, change the container group GID that have the same GID
            echo "GID in use, change the container group GID that have the same GID"
            groupmod -g 4000 $(getent group $HOST_WWW_DATA_GID | cut -d: -f1)
        fi
        echo "host www-data GID != container www-data GID, change local GID"
        # Change www-data gid
        echo "change www-data gid to $HOST_WWW_DATA_GID"
        groupmod -g $HOST_WWW_DATA_GID www-data
    fi
else
    # Group not exists in container, create it with HOST_WWW_DATA_GID
    
    # Check if the HOST_WWW_DATA_GID is in use in the container
    if [ "$(getent group $HOST_WWW_DATA_GID | cut -d: -f1)" != "" ]; then
        # GID in use, change the container group GID that have the same GID
        echo "GID in use, change the container group GID that have the same GID"
        groupmod -g 4000 $(getent group $HOST_WWW_DATA_GID | cut -d: -f1)
    fi
    echo "Group not exists in container, create it with HOST_WWW_DATA_GID"
    # Create www-data group
    groupadd -g $HOST_WWW_DATA_GID www-data
fi


# # Check HOST_USER_GID
# # Check if the HOST_USER_GID is in use in the container
# if [ "$(getent group $HOST_USER_GID | cut -d: -f1)" != "" ]; then
#     # GID in use, change the container group GID that have the same GID
#     echo "GID in use, change the container group GID that have the same GID"
#     groupmod -g 4000 $(getent group $HOST_USER_GID | cut -d: -f1)
# fi
# echo "Create group for HOST_USER_GID"
# # Create www-data group
# groupadd -g $HOST_USER_GID $HOST_USER_GNAME
