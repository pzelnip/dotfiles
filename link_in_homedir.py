
from subprocess import call
import os

def dotfilesdir():
    fromdir = os.path.join(os.getcwd(), "dotfiles")
    todir = os.environ['HOME']
    call(["lndir", fromdir, todir])
    print "Linked %s to %s" % (fromdir, todir)


def bindir():
    fromdir = os.path.join(os.getcwd(), "bin")
    todir = os.path.join(os.environ['HOME'], "bin")
    try:
        os.mkdir(todir)
    except OSError as e:
        pass # directory already exists

    call(["lndir", fromdir, todir])
    print "Linked %s to %s" % (fromdir, todir)


def main():
    dotfilesdir()
    bindir()


if __name__ == "__main__":
    main()
