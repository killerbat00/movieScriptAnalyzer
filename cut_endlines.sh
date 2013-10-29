#!/bin/bash

# Matches and removes 5 lines before the line User Comments
# This line is the last non-script text located in the files.
# This saves the files into a new directory with a new 
# <Script Name>.final.txt extension with all newlines stripped

mkdir processed_scripts/final_scripts

for file in `find processed_scripts/likely_good -type f`; do 
    FNAME=`echo ${file##*/} | cut -d '.' --complement -f2-`
    MID='.mid.txt'
    FIN='.final.txt'
    tac $file | sed '/User Comments/I, +5d' | tac > $FNAME$MID
    sed -e :a -e '/./,$!d;/^\n*$/{$d;N;};/\n$/ba' $FNAME$MID > $FNAME$FIN
    rm $FNAME$MID
    mv $FNAME$FIN processed_scripts/final_scripts/
done
