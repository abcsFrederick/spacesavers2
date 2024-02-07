## spacesavers2_e2e

This is a wrapper to run all the `spacesavers2` commands in the correct order. It automatically:

- adds appropriate prefixes to output files (including time)
- catalogs files in the folder provided
- finds duplicates
- finds high-value duplicates
- creates blamematrix

This is ideal wrapper to be added as a cronjob.

```bash
 % spacesavers2_e2e --help
usage: spacesavers2_e2e [-h] -i INFOLDER [-p THREADS] [-q QUOTA] -o OUTFOLDER

End-to-end run of spacesavers2

options:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Folder to run spacesavers_ls on.
  -p THREADS, --threads THREADS
                        number of threads to use
  -q QUOTA, --quota QUOTA
                        total size of the volume (default = 200 for /data/CCBR)
  -o OUTFOLDER, --outfolder OUTFOLDER
                        Folder where all spacesavers_finddup output files will be saved
```