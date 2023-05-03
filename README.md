# spacesavers2
New improved parallel implementation of [`spacesavers`](https://github.com/CCBR/spacesavers).

> Note: `spacesavers2` requires [python version 3.11](https://www.python.org/downloads/release/python-3110/) or later and the [xxhash](https://pypi.org/project/xxhash/) library. These dependencies are already installed on biowulf. The enviroment for running `spacesavers2` can get set up using:
> ```bash
> alias source_conda='. "/data/CCBR_Pipeliner/db/PipeDB/Conda/etc/profile.d/conda.sh"'
> conda activate py311
> ```
## Basic commands

```bash
% spacesavers2_ls --help
usage: spacesavers2_ls [-h] -f FOLDER [-p THREADS] [-b BUFFERSIZE] [-i IGNOREHEADERSIZE] [-s SE] [-e | --bottomhash | --no-bottomhash]

spacesavers2_ls: get per file info.

options:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        spacesavers2_ls will be run on all files in this folder and its subfolders
  -p THREADS, --threads THREADS
                        number of threads to be used
  -b BUFFERSIZE, --buffersize BUFFERSIZE
                        buffersize for xhash creation
  -i IGNOREHEADERSIZE, --ignoreheadersize IGNOREHEADERSIZE
                        this sized header of the file is ignored before extracting buffer of buffersize for xhash creation (only for special extension files)
  -s SE, --se SE        comma separated list of special extentions
  -e, --bottomhash, --no-bottomhash
                        separately calculated second hash for the bottom/end of the file.

Version: v0.1 Example: % spacesavers2_ls -f /path/to/folder -p 56 -e
```

```bash
% spacesavers2_finddup --help
usage: spacesavers2_finddup [-h] -f LSOUT [-u UID] [-d DEPTH] [-o OUTDIR] [-q QUOTA]

spacesavers2_finddup: find duplicates

options:
  -h, --help            show this help message and exit
  -f LSOUT, --lsout LSOUT
                        spacesavers2_ls output from STDIN or from file
  -u UID, --uid UID     user id or 0 for all users ... if 0 is provided the {sys.argv[1]} is run for all users
  -d DEPTH, --depth DEPTH
                        folder max. depth upto which reports are aggregated
  -o OUTDIR, --outdir OUTDIR
                        output folder
  -q QUOTA, --quota QUOTA
                        total quota of the mount eg. 200 TB for /data/CCBR

Version: v0.1 Example: % spacesavers2_finddup -f /output/from/spacesavers2_ls -o /path/to/output/folder -d 7 -q 10
```


