#!/bin/bash
timestamp=`date +%Y/%m/%d-%H:%M:%S`
wget http://10.22.26.2:8000/scheduler/delete_expired_files
echo "Expired files deleted at $timestamp."