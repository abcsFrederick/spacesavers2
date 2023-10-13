#!/usr/bin/env bash
module load singularity
SINGULARITY_CACHEDIR=/data/CCBR_Pipeliner/SIFS
echo "cd /mnt && Rscript bin/render.R" |\
    singularity exec -C -B $PWD:/mnt,/data/CCBR_Pipeliner/userdata/spacesavers2/:/mnt/data docker://kellysovacool/spacesavers2:0.1.0 bash