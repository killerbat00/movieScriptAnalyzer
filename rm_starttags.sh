#!/bin/bash

# Some of the files are prepended with a <b> tag to change
# the window hash.
# These files are first found with grep, then we conservatively
# remove 5 lines from the top of the file.
# Some files require more than this, but this script can be used again
# to identify them

for file in `grep -ril "<b>" processed_scripts/final_scripts > files.txt`; do
    FNAME=`echo ${file##*/} | cut -d '.' --complement -f2-`
    FIN='.final.txt'
    tail -n +5 $file > $FNAME$FIN
done

