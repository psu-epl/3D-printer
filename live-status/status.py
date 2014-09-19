#!/usr/bin/env python
import argparse
import os

parser = argparse.ArgumentParser(prog='mojo')
parser.add_argument('-l', '--logfile', type=argparse.FileType('r'))
args = vars(parser.parse_args())

log = args['logfile']

for line in reversed(log.readlines()):
    li = line.rstrip().split(' ')

    cmd = li[0]
    if cmd == '$jobStartCmd':
        print "running"
        break
    else:
        print ""
