# Adam's Home Directory Stuff

This repo contains some of the stuff from my home directory on my work machine.

Included are my basic config files and a bin directory that I typically add to my PATH with various tools & utilities.

This was inspired by a number of talks at Polyglot 2013, as well as the discussion at:

http://stackoverflow.com/questions/17082038/efficient-way-to-manage-a-git-repository-for-local-config-files

To copy everything to the current user's home directory, do a:

```
python link_in_homedir.py
```

to create symbolic links from all the files into the home directory of the currently logged in user.
