# :rocket: spacesavers2 :rocket:

## Background

New and improved ultra-fast implementation of [`spacesavers`](https://github.com/CCBR/spacesavers).

> Note: `spacesavers2` requires [python version 3.11](https://www.python.org/downloads/release/python-3110/) or later and the [xxhash](https://pypi.org/project/xxhash/) library.  These dependencies are already installed on biowulf. The enviroment for running `spacesavers2` can get set up on [BIOWULF](https://hpc.nih.gov) using:
> ```bash
> alias source_conda='. "/data/CCBR_Pipeliner/db/PipeDB/Conda/etc/profile.d/conda.sh"'
> conda activate py311
> ```

spacesavers2 has two main commands:

 - [spacesavers_ls](ls.md)
 - [spacesavers_finddup](finddup.md)

spacesavers2 also has the following wrapper scripts:

 - [spacesavers_e2e](e2e.md)

> Please send comment/queries to [Vishal Koparde](mailto:vishal.koparde@nih.gov).