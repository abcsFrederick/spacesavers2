#!/usr/bin/env bash
module load singularity
SINGULARITY_CACHEDIR=/data/CCBR_Pipeliner/SIFS
echo "cd /mnt && Rscript bin/render.R" |\
    singularity exec -C -B /data/CCBR_Pipeliner/spacesavers2-report:/mnt,/data/CCBR_Pipeliner/userdata/spacesavers2/:/mnt/data docker://nciccbr/spacesavers2:0.1.0 bash
