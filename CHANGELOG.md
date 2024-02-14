## spacesavers2 development version

### New features

### Bug fixes

## spacesavers2 0.11.1

### New features

- `spacesavers2_e2e` now shows more defaults in "--help"

### Bug fixes

- grubbers do not include non-duplicate copies (aka hardlinks) (#78, @kopardev)
- blamematix reports numbers correctly (minor bug fix)

## spacesavers2 0.11.0

### New features

- Add `requirements.txt` for easy creation of environment in "spacesavers2" docker (#68, @kopardev)
- `grubbers` has new `--outfile` argument.
- `blamematrix` has now been moved into `mimeo`.
- `mimeo` files.gz always includes the original file as the first one in the filelist.
- `mimeo` now has kronatools compatible output. ktImportText is also run if in PATH to generate HTML report for duplicates only. (#46, @kopardev)
- Update documentation.

### Bug fixes

- `e2e` overhauled, improved and well commented.
- `grubbers` `--limit` can be < 1 GiB (float) (#70, @kopardev)
- `grubbers` output file format changed. New original file column added. Original file is required by `usurp`.
- `mimeo` `--duplicateonly` now correctly handles duplicates owned by different UIDs. (#71, @kopardev)
    - Update `blamematrix` and to account for corrected duplicate handling in `mimeo`.
- `usurp` now uses the new "original file" column from `grubbers` while creating hard-links.
- Total size now closely resembles `df` results (fix #75 @kopardev)
- Files with future timestamps are handled correctly (fix #76, @kopardev)
  
## spacesavers2 0.10.2

- Now tracking user-facing changes with a changelog. (#61, @kelly-sovacool)
- Generated a report of spacesavers metrics on a cron schedule and sent via email. (#36, #48, #60, #63, @kelly-sovacool)
- Print the version. (#40, #41, @kopardev)
- Bugfixes. (#56, @kopardev)
- fix `requirements.txt` to meet GH Dependabot (#66, @kopardev)
- Improvements to grubbers and usurp docs. (#57, @kopardev)

## spacesavers2 0.10.1

Release notes were not written for this version or prior.
