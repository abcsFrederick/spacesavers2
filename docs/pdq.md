## spacesavers2_pdq

pdq = Pretty Darn Quick

This uses `glob` library to list all files in a user-provided folder recursively. 

For each user it gathers information like:
 - total number of files
 - total number of bytes

It is quick tool to gather datapoints to monitor filesystem usage. Typically, can be run once daily and compared with previous days run to find large changes.

### Inputs
 - `--folder`: Path to the folder to run `spacesavers2_pdq` on.
 - `--threads`: `spacesavers2_pdq` uses multiprocessing library to parallelize orchestration. This defines the number of threads to run in parallel.
 - `--outfile`: If not supplied then the optput is written to the screen.

> NOTE: `spacesavers2_pdq` reports errors (eg. cannot read file) to STDERR

```bash
usage: spacesavers2_pdq [-h] -f FOLDER [-p THREADS] [-o OUTFILE] [-v]

spacesavers2_pdq: get quick per user info (number of files and bytes).

options:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        spacesavers2_pdq will be run on all files in this folder and its subfolders
  -p THREADS, --threads THREADS
                        number of threads to be used (default 4)
  -o OUTFILE, --outfile OUTFILE
                        outfile ... catalog file .. by default output is printed to screen
  -v, --version         show program's version number and exit

Version:
    v0.11.5
Example:
    > spacesavers2_pdq -f /path/to/folder -p 4 -o /path/to/output_file
```

### Output

## tab-delimited output (file)

`spacesavers2_pdq` creates one tab seperated output line per user:

```bash
% head -n1 test.out
user1       1386138 6089531321856
user2  230616  2835680212992
user3      1499    126442496
```
The 3 items in the line are as follows:


| Column | Description              | Example                                                                                        |
| ------ | ------------------------ | ---------------------------------------------------------------------------------------------- |
| 1      | username                 | "user1" |
| 2      | total no. of files owned     | 1386138                                                                                          |
| 3      | total no. of bytes occupied      | 6089531321856                                                                                        |
