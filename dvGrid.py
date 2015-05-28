#!/usr/bin/env python

# dvGrid.py creates an array of tiled microscope stage positions from a list of two
# positions for Deltavision Softworx.
# Copyright (C) 2013  Thomas Julou (thomas.julou@normalesup.org)
# 
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.

from optparse import OptionParser
import sys, os.path
import re
import math

# Set options default value
usage = "Usage: %prog [options] posFile\nThe file argument must correspond to a DV position file with at least two positions."
pxSize = 0.064
fieldSize = 1024
overlap = 32

# Read in arguments and options
parser = OptionParser(usage)
parser.add_option("-o", "--out", type="string", dest="outPath", default="",
                  help='specify the output path. Default is the position file name appended with "_grid"')
parser.add_option("-p", "--pixel-size", type="float", dest="pxSize", default=pxSize,
                  help="")
parser.add_option("-s", "--field-size", type="int", dest="fieldSize", default=fieldSize,
                  help="")
parser.add_option("-l", "--field-overlap", type="int", dest="overlap", default=overlap,
                  help="")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()
if len(args) == 1:
    inPath = args[0]
else:
    sys.exit("Error: You must provide a unique file name as argument.")
if os.path.isfile(inPath):
    inFile = open(inPath, mode='rb')
    lines = inFile.readlines()
    inFile.close()
else:
    sys.exit("Error: the argument (%s) is not a valid path to a file." % inPath)
outPath = options.outPath
pxSize = options.pxSize
fieldSize = options.fieldSize
overlap = options.overlap
verbose = options.verbose

if verbose:
    print 'dvGrid generating a grid of positions after %s' % inPath
    print '\tPixel size: %.3fum\n\tField size: %dpx\n\tOverlap between fields: %dpx\n' % (pxSize, fieldSize, overlap)

if len(lines) > 2 and verbose:
    print 'Warning: more than 2 positions in the list. Only the first two are considered.'


# Interpolate grid positions
try:
    str1 = re.split(' *', str.lstrip(lines[0]))
    x1 = float(str1[1]); y1 = float(str1[2]); z1 = float(str1[3]);
    str2 = re.split(' *', str.lstrip(lines[1]))
    x2 = float(str2[1]); y2 = float(str2[2]); z2 = float(str2[3]);
except IndexError:
    sys.exit("\nError: Positions parsing failed.\nTip: did you provide a valid DV positions file as argument?")
    
fieldSize_um = fieldSize * pxSize
fieldShift = (fieldSize - overlap) * pxSize # in um
nx = int(math.ceil(abs(x2 - x1) / fieldShift))
ny = int(math.ceil(abs(y2 - y1) / fieldShift))
z = (z1 + z2) / 2

if outPath == "":
    dirName, fileName = os.path.split(inFile.name)
    fileName, fileExt = os.path.splitext(fileName)
    outPath = os.path.join(dirName, '%s_grid%s' % (fileName, fileExt))
outFile = open(outPath, 'w')

c = 0
for i in range(nx):
    for j in range(ny):
        c = c + 1
        x = min(x1, x2) + fieldShift * i
        y = min(y1, y2) + fieldShift * j
        xs = str('%+.2f' % x).rjust(11)
        ys = str('%+.2f' % y).rjust(11)
        zs = str('%+.2f' % z).rjust(10)
        line = '%4d:%s%s%s  \n' % (c, xs, ys, zs)
        outFile.write(line)

outFile.close()
if verbose:
    print 'Grid with %d positions written to %s' % (c, outPath)

