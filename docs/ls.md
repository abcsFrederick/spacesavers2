## spacesavers2_ls

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
 - `--folder`: Path to the folder to run `spacesavers2_ls` on.
 - `--threads`: `spacesavers2_ls` uses multiprocessing library to parallelize orchestration. This defines the number of threads to run in parallel.
 - `--buffersize`: This defines the size of the top (or bottom) chunk of the file to be used to by xxHash. (default 128 KB)
 - `--ignoreheadersize`: This defines the size of the top of the file to be **ignored** before reading the top chunk for xxHash calculation. This is useful for ignore the header portion of files like BAM or BIGWIG which may have the same top chunk (Eg. samples aligned to the same reference index will generate BAMs with the same header hence original `spacesaver`, which only looks at the top chunk, may call them duplicates. `spacesavers2` tries to do a better job at this.). (default 1 MB)
 - `--se`: Comma-separated special extensions for home `spacesavers2` ignores the headers before extracting the top chunk for xxHash calculation. The default is "bam,bai,bigwig,bw,csi".
 - `--bottomhash`: Default False. Use the bottom chunk along with the top chunk of the file for xxHash calculation.
 - `--outfile`: If not supplied then the optput is written to the screen.

> NOTE: `spacesavers2_ls` reports errors (eg. cannot read file) to STDERR

```bash
 % spacesavers2_ls --help
usage: spacesavers2_ls [-h] -f FOLDER [-p THREADS] [-b BUFFERSIZE] [-i IGNOREHEADERSIZE] [-s SE] [-o OUTFILE] [-e | --bottomhash | --no-bottomhash]

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
  -o OUTFILE, --outfile OUTFILE
                        outfile ls_out file .. by default output is printed to screen
  -e, --bottomhash, --no-bottomhash
                        separately calculated second hash for the bottom/end of the file.

Version: v0.3 Example: % spacesavers2_ls -f /path/to/folder -p 56 -e
```

### Output

`spacesavers2_ls` creates one semi-colon seperated output line per input file. Here is an example line:

```bash
% head -n1 test.ls_out
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

> NOTE: Some files may have ";" in their name, hence adding quotes around the absolute file path.