#!/usr/bin/python

from __future__ import print_function
import json
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import sys


def main():
    args = sys.argv[1:]
    try:
        # Setup argument parser
        parser = ArgumentParser(description='DB Pass',
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("--node", nargs='*', help="Specifies the node name")
        
        # Process arguments
        args = parser.parse_args(args)

        if args.node:
            with open('/Users/aparkin/temp/sandbox/ss-chef/nodes/%s.zeromember.com.json' % args.node[0], 'r') as fobj:
                contents = json.load(fobj)
                if contents.has_key('mongodb'):
                    if contents['mongodb'].has_key('admin'):
                        if contents['mongodb']['admin'].has_key('password'):
                            print (contents['mongodb']['admin']['password'])

    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    main()