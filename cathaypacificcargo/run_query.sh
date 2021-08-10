#!/bin/bash

source $HOME/.profile
workerfolder="$HOME/awb_crawler"
detial_query=$(ps aux | grep [a]wb_detial_query)
now=$(date '+%Y/%m/%d %H:%M:%S')
echo "time: $now" >> $HOME/awb_crawler/cathaypacificcargo/run_query.log
if [ -z "$detial_query" ]
then
    echo "awb_detial_query not running....." >> $workerfolder/cathaypacificcargo/run_query.log
    echo "execute: python3 awb_detial_query.py" >> $workerfolder/cathaypacificcargo/run_query.log
    /usr/bin/python3 $workerfolder/cathaypacificcargo/awb_detial_query.py
fi

mutlip_query=$(ps aux | grep [a]wb_mutlip_query)
if [ -z "$mutlip_query" ]
then
    echo "awb_mutlip_query not running....." >> $workerfolder/cathaypacificcargo/run_query.log
    echo "execute: python3 awb_mutlip_query.py" >> $workerfolder/cathaypacificcargo/run_query.log
    /usr/bin/python3 $workerfolder/cathaypacificcargo/awb_mutlip_query.py
fi