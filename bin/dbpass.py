#!/usr/bin/python

from __future__ import print_function
import json
import sys


def main():
    if sys.argv < 2:
        print("specify node")
        return

    node = sys.argv[1]

    try:
        with open('/Users/aparkin/temp/sandbox/ss-chef/nodes/%s.zeromember.com.json' % node, 'r') as fobj:
            contents = json.load(fobj)
            if contents.has_key('mongodb'):
                if contents['mongodb'].has_key('admin'):
                    if contents['mongodb']['admin'].has_key('password'):
                        print (contents['mongodb']['admin']['password'])

    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    main()