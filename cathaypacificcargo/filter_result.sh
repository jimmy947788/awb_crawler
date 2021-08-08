#!/bin/bash

source /home/pi/.profile
output_file="/var/www/html/awb-lhr-hkg.txt"
interesting_detial_result_file="/home/pi/awb_crawler/cathaypacificcargo/data/interesting_detial_result.csv"
multi_query_result_file="/home/pi/awb_crawler/cathaypacificcargo/data/multi_query_result_6.csv"
interesting_awb_list_file="/home/pi/awb_crawler/cathaypacificcargo/data/interesting_awb_list.txt"
filter_key="LHR,HKG"
result_count=$(tr '[:space:]' '[\n*]' < $interesting_detial_result_file | grep -i -c $filter_key)
filter2_totals=$(wc -l $interesting_detial_result_file | awk '{print$1}')
filter2_totals2=$(wc -l $interesting_awb_list_file | awk '{print$1}')
filter1_totals=$(wc -l $multi_query_result_file | awk '{print$1}')
echo "last update time: $(date '+%Y/%m/%d %H:%M:%S')" > $output_file
echo "download counts : $filter1_totals " >> $output_file 
echo "checked location counts: $filter2_totals / $filter2_totals2" >> $output_file 
echo "found $filter_key counts: $result_count" >> $output_file 
echo "" >> $output_file 
cat $interesting_detial_result_file | grep "$filter_key" >> $output_file

cp $multi_query_result_file "/var/www/html/no-detial.txt"
cp $interesting_detial_result_file "/var/www/html/awb-all.txt"