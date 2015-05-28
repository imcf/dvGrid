# dvGrid
dvGrid creates an array of tiled microscope stage positions from a list of two positions for Deltavision Softworx.

```
Usage: dvGrid.py [options] posFile
The file argument must correspond to a DV position file with at least two positions.

Options:
  -h, --help            show this help message and exit
  -o OUTPATH, --out=OUTPATH
                        specify the output path. Default is the position file
                        name appended with "_grid"
  -p PXSIZE, --pixel-size=PXSIZE
  -s FIELDSIZE, --field-size=FIELDSIZE
  -l OVERLAP, --field-overlap=OVERLAP
  -q, --quiet           don't print status messages to stdout
```