#!/usr/bin/python2.6
import sys, os, re

# Extracts all text from ALL SCRIPTS to Back to IMSDb.
# This chunk of text encompasses the vast majority of the script.
# This file is invoked through the bash script pp.sh
#
# This saves a new copy of the script into a processed_scripts
# directory with a new .pp extension.

def main(infile):
    with open(infile) as fp:
        for result in re.findall('ALL SCRIPTS(.*?)Back to IMSDb', fp.read(), re.S):
            ofp = open(os.path.join('processed_scripts', infile.split('/')[1]+'.pp'), 'w')
            ofp.write(result)

if __name__=='__main__':
    if not os.path.isdir(os.path.join(os.getcwd(), 'processed_scripts')):
        os.mkdir(os.path.join(os.getcwd(), 'processed_scripts'))
    main(sys.argv[1])
