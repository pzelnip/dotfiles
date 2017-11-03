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

Edit: most recently for setting up a new machine at a new job I skipped this step and just copied everything in `dotfiles` to `~` and everything in `bin/` to `~/bin` instead of simlinking.  This is partly as A) installing Quartz toolkit just to get lndir is crazysauce, and B) I've found that it's rare I update the stuff in this repo, and it's not uncommon to want to make "custom" changes to files that are specific to a machine.  As such it sometimes makes more sense to use the stuff here as "starting points", and revise as needed on a particular machine.

## Caveats/Issues/Notes

### Username

Previously, some of the scripts assume a username of "aparkin", and failure to run them under a user with this name would result in weird stuff happening (ie - stuff breaks).  I *think* I have resolved this issue, however, this is (at the time of this writing) untested.

### lndir

```lndir``` is required for the scripts to work.  On OSX Lion, this command is (I believe) included by default.  On Mountain Lion or later you'll have to install the Quartz tookit to get it, see:

http://xquartz.macosforge.org/landing/

### Python Stuff 

There's various Python utilities required:

```
$ sudo easy_install pip
$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
```
### iTerm2

I use [iTerm2](http://www.iterm2.com/#/section/home) as my terminal of choice, and my config can be found in ```iterm/```

At the time of writing the only way to restore this config is to copy it (or simlink it) to ```~/Library/Preferences/``` for example:

```
$ ln -s com.googlecode.iterm2.plist ~/Library/Preferences/
```

Edit: I've given up on this as literally *every* single time I've tried simlinking to the same settings file it's borked.  I really wish there was a reliable way to easily save & restore iterm settings, but I have yet to find it.

## Other Setup Stuff

### Amphetamine

Amphetamine: https://itunes.apple.com/ca/app/amphetamine/id937984704?mt=12

Previously I used Caffeine from the app store: http://itunes.apple.com/us/app/caffeine/id411246225 but that appears to now be deprecated

### Calendar in menubar

I've moved through various solutions for this, most recently Calendar 2: https://qbix.com/calendar (pick Calendar 2 once you get to the app store, should be free)

https://www.mowglii.com/itsycal/ is an alternative.

Previously used MenuCalendarClock for iCal ( http://download.cnet.com/MenuCalendarClock-for-iCal/3000-2124_4-18953.html ) but this appears to be abandonware now

Some settings for it:

- Custom clock format: %b %d %1I:%M:%S %p
- Under display -> Advanced, make sure "Hide Dock Icon" is selected

### CPULed

Install CPULED from the appstore: https://itunes.apple.com/ca/app/cpu-led/id448189857?mt=12

### MacVim

https://code.google.com/p/macvim/

### GitX (L)

http://gitx.laullon.com/

### Hex Fiend 

http://ridiculousfish.com/hexfiend/

### Spectacle

http://spectacleapp.com/

### Fluid

http://fluidapp.com/

### Truecrypt

This ones complicated now.  Get the DMG from Gibson Research Corp:

https://www.grc.com/misc/truecrypt/truecrypt.htm

Now, if you're on Yosemite or later, you'll find that the installer borks.  To fix:

Open the .dmg
You’ll find the .mpkg. Right*click and “Show Package Contents”
Open Contents Dir
Open Packages Dir
Install each of the 4 packages in this order: OSXFUSECore.pkg, OSXFUSEMacFUSE.pkg, MacFUSE.pkg, TrueCrypt.pkg (It is possible MacFUSE.pkg will install the two before it, but we ran each to play it safe.).

Source (https://lazymind.me/2014/10/install-truecrypt-on-mac-osx-yosemite-10-10/)

## Other Examples of This

I'm not the first to throw my config/setup stuff into a source control repo, others to look at for inspiration:

https://bitbucket.org/j/dotfiles/src

https://github.com/garybernhardt/dotfiles

delete me later
