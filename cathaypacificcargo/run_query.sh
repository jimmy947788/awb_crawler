#!/bin/bash

detial_query=$(ps aux | grep [a]wb_detial_query)
now=$(date '+%Y/%m/%d %H:%M:%S')
if [ -z "$detial_query" ]
then
    echo "time: $now"
    echo "awb_detial_query not running....."
    echo "execute: python3 awb_detial_query.py"
    /usr/bin/python3 $HOME/awb_crawler/cathaypacificcargo/awb_detial_query.py
fi