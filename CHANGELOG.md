## spacesavers2 development version

### New features

### Bug fixes

## spacesavers2 0.11.0

### New features

- adding `requirements.txt` for easy creation of environment in "spacesavers2" docker (#68, @kopardev)
- `grubbers` has new `--outfile` argument.
- `blamematrix` has 3 new arguments `--humanreable`, `--includezeros` and `--outfile`.
- `mimeo` files.gz always includes the original file as the first one in the filelist.
- `mimeo` now has kronatools compatible output. ktImportText is also run if in PATH to generate HTML report for duplicates only. (#46, @kopardev)
- documentation updated.

### Bug fixes

- `grubbers` `--limit` can be < 1 GiB (float) (#70, @kopardev)
- `grubbers` output file format changed. New original file column added. Original file is required by `usurp`
- `mimeo` `--duplicateonly` logic fix (#71, @kopardev)
- `blamematrix` fixed to account for changes due to #71
- `usurp` fixed to account for changes due to #71. Now using the new "original file" column while creating hard-links.
- `e2e` overhauled, improved and well commented.
  
## spacesavers2 0.10.2

- Now tracking user-facing changes with a changelog. (#61, @kelly-sovacool)
- Generated a report of spacesavers metrics on a cron schedule and sent via email. (#36, #48, #60, #63, @kelly-sovacool)
- Print the version. (#40, #41, @kopardev)
- Bugfixes. (#56, @kopardev)
- fix `requirements.txt` to meet GH Dependabot (#66, @kopardev)
- Improvements to grubbers and usurp docs. (#57, @kopardev)

## spacesavers2 0.10.1

Release notes were not written for this version or prior.
