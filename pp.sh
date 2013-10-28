#!/bin/bash

# Lists all scripts in scripts/ directory and invokes postproc.py on each
for f in `find scripts/`;
do /localhome/bmorrow/imsdb_parse/postpros.py $f;
done 
