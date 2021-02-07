#!/usr/bin/env python3

"""gi - correct those git typos.

I have a bad habit of typing:

gi tstatus
or
gi t status

instead of

git status

This command just tries to guess if you meant to type git instead of gi,
and if so, passes whatever you would've passed to git to git.

Very similar to https://github.com/nvbn/thefuck
"""

import sys
import os


def main():
    cmd = " ".join(sys.argv[1:]).strip()
    if not cmd.lower().startswith('t'):
        print('what were you trying to do?')
        return 1

    cmd = "git " + cmd[1:].strip()
    print("gi!  replacing with " + cmd)
    os.system(cmd)

if __name__ == "__main__":
    exit(main())
