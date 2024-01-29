#!/usr/bin/env bash
# to be executed from /data/CCBR_Pipeliner/Tools/spacesavers2/report
# Usage: bash bin/render_report_biowulf.sh
module load singularity
SINGULARITY_CACHEDIR=/data/CCBR_Pipeliner/SIFS

# render report
echo "cd /mnt && \
    Rscript bin/render.R \
    " |\
    singularity exec -C -B $PWD:/mnt,/data/CCBR_Pipeliner/userdata/spacesavers2/:/mnt/data docker://nciccbr/spacesavers2:0.1.1 bash
