## spacesavers2_catalog

This uses `glob` library to list all files in a user-provided folder recursively. 

For each file it gathers information like:
 - filesize
 - check if it is symlink
 - inode
 - creation and modificatino time
 - user id
 - group id

For each file it also computes a unique hash (using xxHash library) for:
 - top chunk of the file
 - bottom chunk of the file (`-e` option)

### Inputs
 - `--folder`: Path to the folder to run `spacesavers2_catalog` on.
 - `--threads`: `spacesavers2_catalog` uses multiprocessing library to parallelize orchestration. This defines the number of threads to run in parallel.
 - `--buffersize`: This defines the size of the top (or bottom) chunk of the file to be used to by xxHash. (default 128 KB)
 - `--ignoreheadersize`: This defines the size of the top of the file to be **ignored** before reading the top chunk for xxHash calculation. This is useful for ignore the header portion of files like BAM or BIGWIG which may have the same top chunk (Eg. samples aligned to the same reference index will generate BAMs with the same header hence original `spacesaver`, which only looks at the top chunk, may call them duplicates. `spacesavers2` tries to do a better job at this.). (default 1 MB)
 - `--se`: Comma-separated special extensions for home `spacesavers2` ignores the headers before extracting the top chunk for xxHash calculation. The default is "bam,bai,bigwig,bw,csi".
 - `--bottomhash`: Default False. Use the bottom chunk along with the top chunk of the file for xxHash calculation.
 - `--outfile`: If not supplied then the optput is written to the screen.
 - `--brokenlink`: Default False. Create a file listing broken symlinks per-user.
 - `--geezer`: Default False. Create a file listing really old files per-user. Output files have 3 columns: age, size, path
   - `--geezerage`: Default 5 * 365. age in days to be considered a geezer file.
   - `--geezersize`: Default 10 MiB. minimum size in bytes of geezer file to be reported.

> NOTE: `spacesavers2_catalog` reports errors (eg. cannot read file) to STDERR

```bash
usage: spacesavers2_catalog [-h] -f FOLDER [-p THREADS] [-b BUFFERSIZE] [-i IGNOREHEADERSIZE] [-x SE] [-s ST_BLOCK_BYTE_SIZE] [-o OUTFILE]
                            [-e | --bottomhash | --no-bottomhash] [-l | --brokenlink | --no-brokenlink] [-g | --geezers | --no-geezers]
                            [-a GEEZERAGE] [-z GEEZERSIZE] [-v]

spacesavers2_catalog: get per file info.

options:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        spacesavers2_catalog will be run on all files in this folder and its subfolders
  -p THREADS, --threads THREADS
                        number of threads to be used (default 4)
  -b BUFFERSIZE, --buffersize BUFFERSIZE
                        buffersize for xhash creation (default=128 * 1028 bytes)
  -i IGNOREHEADERSIZE, --ignoreheadersize IGNOREHEADERSIZE
                        this sized header of the file is ignored before extracting buffer of buffersize for xhash creation (only for special
                        extensions files) default = 1024 * 1024 * 1024 bytes
  -x SE, --se SE        comma separated list of special extensions (default=bam,bai,bigwig,bw,csi)
  -s ST_BLOCK_BYTE_SIZE, --st_block_byte_size ST_BLOCK_BYTE_SIZE
                        st_block_byte_size on current filesystem (default 512)
  -o OUTFILE, --outfile OUTFILE
                        outfile ... catalog file .. by default output is printed to screen
  -e, --bottomhash, --no-bottomhash
                        separately calculated second hash for the bottom/end of the file.
  -l, --brokenlink, --no-brokenlink
                        output per-user broken links list.
  -g, --geezers, --no-geezers
                        output per-user geezer files list.
  -a GEEZERAGE, --geezerage GEEZERAGE
                        age in days to be considered a geezer file (default 5yrs ... 5 * 365).
  -z GEEZERSIZE, --geezersize GEEZERSIZE
                        minimum size in bytes of geezer file to be reported (default 10MiB ... 10 * 1024 * 1024).
  -v, --version         show program's version number and exit

Version:
    v0.11.4
Example:
    > spacesavers2_catalog -f /path/to/folder -p 56 -e -l -g
```

### Output

## catalog file

`spacesavers2_catalog` creates one semi-colon seperated output line per input file. Here is an example line:

```bash
% head -n1 test.catalog
"/data/CBLCCBR/kopardevn_tmp/spacesavers2_testing/_data_CCBR_Pipeliner_db_PipeDB_Indices.ls.old";False;1653453;47;372851499;1;1;5;5;37513;57886;4707e661a1f3beca1861b9e0e0177461;52e5038016c3dce5b6cdab635765cc79;
```
The 13 items in the line are as follows:


| Column | Description              | Example                                                                                        |
| ------ | ------------------------ | ---------------------------------------------------------------------------------------------- |
| 1      | File absolute path       | "/data/CBLCCBR/kopardevn_tmp/spacesavers2_testing/_data_CCBR_Pipeliner_db_PipeDB_Indices.ls.old" |
| 2      | Is file a symlink?       | FALSE                                                                                          |
| 3      | file size in bytes       | 1653453                                                                                        |
| 4      | file device              | 47                                                                                             |
| 5      | file inode               | 372851499                                                                                      |
| 6      | number of hardlinks      | 1                                                                                              |
| 7      | access age in days       | 1                                                                                              |
| 8      | modification age in days | 5                                                                                              |
| 9      | creation age in days     | 5                                                                                              |
| 10     | user id                  | 37513                                                                                          |
| 11     | group id                 | 57886                                                                                          |
| 12     | top chunk xxHash         | 4707e661a1f3beca1861b9e0e0177461                                                               |
| 13     | bottom chunk xxHash      | 52e5038016c3dce5b6cdab635765cc79                                                               |

> NOTE: Some files may have ";" or spaces in their name, hence adding quotes around the absolute file path.

## broken links file

  - simply lists the paths which are symbolic links, but the destination files do not exist anymore!
  - one file per username.

> DISCLAIMER:
>  - may contain false-positives if the user running `spacesavers2_catalog` does not have read access to the symlinks destination

## geezer file

  - lists really old files (default > 5 years).
  - list has 3 columns: age, size and path.
  - one file per username.
