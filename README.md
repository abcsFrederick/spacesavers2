# spacesavers2

New improved parallel implementation of [`spacesavers`](https://github.com/CCBR/spacesavers). `spacesavers` is soon to be decommissioned!

> Note: `spacesavers2` requires [python version 3.11](https://www.python.org/downloads/release/python-3110/) or later and the [xxhash](https://pypi.org/project/xxhash/) library. These dependencies are already installed on biowulf (as a conda env). The enviroment for running `spacesavers2` can get set up using:
> ```bash
> . "/data/CCBR_Pipeliner/db/PipeDB/Conda/etc/profile.d/conda.sh" && \
> conda activate py311
> ```
## `spacesavers2` has the following Basic commands:

- spacesavers2_ls
- spacesavers2_finddup
- spacesavers2_grubbers
- spacesavers2_blamematrix
- spacesavers2_e2e

## `spacesavers2` typical workflow looks like this:

![](docs/assets/images/spacesavers2.png)

Detailed documentation can be found [here](). Please reach out to [Vishal Koparde](mailto:vishal.koparde@nih.gov) with queries/comments.
