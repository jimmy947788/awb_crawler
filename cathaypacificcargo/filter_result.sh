#!/bin/bash

source /home/pi/.profile
output_file="/var/www/html/awb-lhr-hkg.txt"
interesting_detial_result_file="/home/pi/awb_crawler/cathaypacificcargo/data/interesting_detial_result.csv"
multi_query_result5_file="/home/pi/awb_crawler/cathaypacificcargo/data/multi_query_result_5.csv"
multi_query_result6_file="/home/pi/awb_crawler/cathaypacificcargo/data/multi_query_result_6.csv"
interesting_awb_list_file="/home/pi/awb_crawler/cathaypacificcargo/data/interesting_awb_list.txt"
filter_key="LHR,HKG"
result_count=$(tr '[:space:]' '[\n*]' < $interesting_detial_result_file | grep -i -c $filter_key)
#echo "result_count : $result_count"
filter2_totals=$(wc -l $interesting_detial_result_file | awk '{print$1}')
#echo "filter2_totals : $filter2_totals"
filter2_totals2=$(wc -l $interesting_awb_list_file | awk '{print$1}')
#echo "filter2_totals2 : $filter2_totals2"
multi_query_result5_totals=$(wc -l $multi_query_result5_file | awk '{print$1}')
#echo "multi_query_result5_totals : $multi_query_result5_totals"
multi_query_result6_totals=$(wc -l $multi_query_result6_file | awk '{print$1}')
#echo "multi_query_result6_totals : $multi_query_result6_totals"
echo "last update time: $(date '+%Y/%m/%d %H:%M:%S')" > $output_file
echo "AWB 5000000 - 6000000 downloads records : $multi_query_result5_totals " >> $output_file 
echo "AWB 6000000 - 7000000 downloads records : $multi_query_result6_totals " >> $output_file 
echo "checked location counts: $filter2_totals / $filter2_totals2" >> $output_file 
echo "found $filter_key counts: $result_count" >> $output_file 
echo "" >> $output_file 
cat $interesting_detial_result_file | grep "$filter_key" >> $output_file
cp $interesting_detial_result_file "/var/www/html/awb-all.txt"