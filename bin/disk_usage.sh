#!/usr/bin/env bash
today=`date +"%Y-%m-%d %H:%M:%S"`

df /data/CCBR |\
  awk -v today="$today" 'NR==1{$(NF+1)="datetime"} NR>1{$(NF+1)=today}1' |\
  sed -E 's/Mounted on/Mounted_on/' |\
  sed -E 's/ +/\t/g' |\
  tail -n 1 \
  >> results/disk_usage.tsv