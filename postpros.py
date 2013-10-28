#!/usr/bin/python2.6
import sys, os, re

def main(infile):
    with open(infile) as fp:
        for result in re.findall('ALL SCRIPTS(.*?)Back to IMSDb', fp.read(), re.S):
            ofp = open(os.path.join('processed_scripts', infile.split('/')[1]+'.pp'), 'w')
            ofp.write(result)

if __name__=='__main__':
    if not os.path.isdir(os.path.join(os.getcwd(), 'processed_scripts')):
        os.mkdir(os.path.join(os.getcwd(), 'processed_scripts'))
    main(sys.argv[1])
