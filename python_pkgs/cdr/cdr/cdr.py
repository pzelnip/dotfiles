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

that contains "foo" will get opened up in VS Code.  Directories to search are
specified in ~/.cdr.json, which is a JSON file containing two keys: basepaths
and fullpaths.  "basepaths" will be expanded to search all 1st-level subdirectories
and fullpaths are searched as-is.  So the above 3 paths would be specified as:

{
    "basepaths": [
        "~/temp/sandbox",
        "/Volumes/CaseSensitive/sandbox"
    ],
    "fullpaths": [
        "~/dotfiles"
    ]
}

~ will be expanded to the full user's home directory (Pathlib's expanduser() is
called on the path string)
"""

import json
import os
import sys
from collections import namedtuple
from pathlib import Path

from bullet import Bullet

Match = namedtuple("Match", "name path".split())

CONFIG_FILE_NAME = "~/.cdr.json"


def get_paths():
    def expand_paths(pathnames):
        # expand home directory & remove dupes
        pathnames = {Path(path).expanduser() for path in pathnames}
        # filter out non-existant paths
        return [path for path in pathnames if path.exists() and path.is_dir()]

    configpath = Path(CONFIG_FILE_NAME).expanduser()
    if not configpath.exists():
        raise RuntimeError(f"{configpath} does not exist")

    with open(configpath, "r") as fobj:
        data = json.loads(fobj.read())
    data["basepaths"] = expand_paths(data["basepaths"])
    data["fullpaths"] = expand_paths(data["fullpaths"])

    result = [Match(f.name, f) for p in data["basepaths"] for f in p.iterdir()] + [
        Match(path.name, path) for path in data["fullpaths"]
    ]

    return result


def is_match(searchterm, match):
    """The search logic.

    Right now this is brain-dead simple, but extracted this fn
    so that it might be made more sophisticated in the future.
    """
    return searchterm.lower() in match.name.lower()


def get_match(searchterm, all_paths):
    match = None
    matches = [match for match in all_paths if is_match(searchterm, match)]
    if len(matches) > 1:
        result = Bullet(
            prompt="Multiple matches, please select:",
            margin=2,
            pad_right=5,
            choices=[match.name for match in matches],
            bullet="★",
            return_index=True,
        ).launch()
        match = matches[result[1]]
    elif len(matches) == 1:
        match = matches[0]
    return match


def main():
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <searchterm>")
        return 1

    searchterm = sys.argv[1]
    all_paths = get_paths()

    print(f'Searching for "{searchterm}" in the following directories:\n')
    for match in all_paths:
        print(match.path)
    print()

    match = get_match(searchterm, all_paths)
    if match:
        cmd = f"code {match.path}"
        print(f'Executing "{cmd}"')
        os.system(cmd)
        return 0
    else:
        print("no match")
        return 1


if __name__ == "__main__":
    exit(main())
