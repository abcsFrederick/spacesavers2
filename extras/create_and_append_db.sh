#!/bin/bash
# This script:
# 1. creates a sqlite3 database using `spacesavers2_pdq_create_db`
# 2. updates the database for "CCBR" mount related datapoints
# 3. updates the database for "CCBR_Pipeliner" mount related datapoints

module load ccbrpipeliner/6
BIN="/data/CCBR_Pipeliner/Tools/spacesavers2/pdq_db/bin"
DB="/data/CCBR_Pipeliner/userdata/spacesavers2_pdq/pdq.db"

if [[ "1" == "0" ]];then
# Step 1.
${BIN}/spacesavers2_pdq_create_db -f $DB
fi

# Step 2.
for f in `ls /data/CCBR_Pipeliner/userdata/spacesavers2_pdq/_data_CCBR.*.tsv*`
do
	bn=$(basename $f)
	echo $bn
	dt=$(echo $bn|awk -F"." '{print $2}')
	dm="CCBR"
	${BIN}/spacesavers2_pdq_update_db \
		--tsv $f \
	       	--database $DB \
		--datamount $dm --date $dt
done

# Step 3.
for f in `ls /data/CCBR_Pipeliner/userdata/spacesavers2_pdq/_data_CCBR_Pipeliner.*.tsv*`
do
	bn=$(basename $f)
	echo $bn
	dt=$(echo $bn|awk -F"." '{print $2}')
	dm="CCBR_Pipeliner"
	${BIN}/spacesavers2_pdq_update_db \
		--tsv $f \
	       	--database $DB \
		--datamount $dm --date $dt
done
