#!/usr/bin/python

import pstats
import sys

def showHelp(pname):
    print "Usage: %s <statfile> <sortcol> <numtoshow>" % (pname) 
    print ""
    print "Valid columns include:"
    print "time - total time inside each method"
    print "cumulative - cumulative time inside each method (includes time in called methods)"
    print "file - sort by module file name"
    print "calls - sort by call count"
    print "module - sort by module name (same as file?)"
    print "pcalls - primitive call count (same as calls?)"
    print "line - sort by line number"
    sys.exit()

if __name__ == "__main__":
    numargs = len(sys.argv)

    if numargs <= 1:
        showHelp(sys.argv[0])

    numLines = None
    header = "time"
    if numargs == 4:
        numLines = int(sys.argv[3])
    if numargs >= 3:
        header = sys.argv[2] 

    p = pstats.Stats(sys.argv[1])
    p.sort_stats(header).print_stats(numLines)
