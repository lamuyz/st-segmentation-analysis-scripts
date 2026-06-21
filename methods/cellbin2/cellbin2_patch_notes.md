# CellBin2 patch notes

This file records the local changes made to the CellBin2 runner used in this project.

## GEM reading

- missing `#OffsetX` / `#OffsetY` is treated as `0`
- float count values are rounded before writing into the matrix

## Intermediate files

- visual GEF generation was limited to `[1, 10, 20, 50, 100, 200]`
- readable temporary tissue GEF files are reused
- legacy `*_mask_adjust.tif` files are accepted

## Fallbacks

- `extract4stitched()` uses a fallback path if feature detection fails
- registration uses a no-registration path if it returns `None`

These changes were added so CellBin2 could run on the datasets used in this project.
