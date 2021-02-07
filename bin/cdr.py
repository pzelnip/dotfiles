#!/usr/bin/env python3

"""cdr - handy way to launch VS Code with a given directory.

Does a fuzzy (substring) search, if any subdirectory contains the search term,
will open VS Code in that directory.

Works with Python 3.5+ and must have the VS code shell command set up (open the
command pallette and search for "Shell Command: Install 'code' command in PATH")

For example, I often have a directory in ~/temp/sandbox where I git clone most
repos I work on.  As well I have a repo checked out at ~/dotfiles.  I also
sometimes have a drive mounted in /Volumes/CaseSensitive which contains a
sandbox directory containing some checked out repos.  This script allows me to
do something like:

cdr.py foo

and the first directory in:

~/temp/sandbox/*
~/dotfiles
/Volumes/CaseSensitive/sandbox/*

that contains "foo" will get opened up in VS Code.
"""

import sys
import os
from pathlib import Path


# The base directories to search for subdirectories in
BASE_PATHS = [Path.home() / "temp" / "sandbox", Path("/Volumes/CaseSensitive/sandbox")]

# Raw full paths to add to the search list (ie not subdirectories)
FULL_PATHS = [Path.home() / "dotfiles"]


def main():
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <searchterm>")
        return 1

    searchterm = sys.argv[1]
    paths = [p for p in BASE_PATHS if p.exists()]
    mappings = {f.name: f for p in paths for f in p.iterdir() if f.is_dir()}
    mappings.update({path.name: path for path in FULL_PATHS})

    print(f'Searching for "{searchterm}" in the following directories:\n')
    for path in mappings.values():
        print(path)

    print()
    for name, path in mappings.items():
        if searchterm.lower() in name.lower():
            cmd = f"code {path}"
            print(f'Executing "{cmd}"')
            os.system(cmd)
            return 0
    print("no match")
    return 1


if __name__ == "__main__":
    exit(main())
