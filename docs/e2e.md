## spacesavers2_e2e

This is a wrapper to run `spacesavers2_ls` followed by `spacesavers2_finddup`. It automatically:

- loads appropriate env on BIOWULF
- adds appropriate prefixes to output files (including time)

This is ideal wrapper to be added as a cronjob.

```bash
 % spacesavers2_e2e --help
usage: spacesavers2_e2e [-h] -i INFOLDER [-p THREADS] [-q QUOTA] -o OUTFOLDER

End-to-end run of spacesavers2

options:
  -h, --help            show this help message and exit
  -i INFOLDER, --infolder INFOLDER
                        Folder to run spacesavers_ls on.
  -p THREADS, --threads THREADS
                        number of threads to use
  -q QUOTA, --quota QUOTA
                        total size of the volume (default = 200 for /data/CCBR)
  -o OUTFOLDER, --outfolder OUTFOLDER
                        Folder where all spacesavers_finddup output files will be saved
```