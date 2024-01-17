#!/usr/bin/env bash
# to be executed from /data/CCBR_Pipeliner/Tools/spacesavers2/report
# Usage: bash bin/render_report_biowulf.sh
module load singularity
SINGULARITY_CACHEDIR=/data/CCBR_Pipeliner/SIFS

today=$(date +'%Y-%m-%d')
year=$(date +'%Y')
mkdir -p docs/$year
html_filename="docs/${year}/report_${today}.html"
receiver_email="kelly.sovacool@nih.gov"

echo "cd /mnt && \
    Rscript bin/render.R && \
    cp docs/report.html $html_filename && \
    python src/send_email.py $html_filename $receiver_email " |\
    singularity exec -C -B $PWD:/mnt,/data/CCBR_Pipeliner/userdata/spacesavers2/:/mnt/data docker://nciccbr/spacesavers2:0.1.1 bash
