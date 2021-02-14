# Adam's Home Directory Stuff

This repo contains some of the stuff from my home directory on most machines
(primarily Mac machines) I use.

Included are my basic config files and a bin directory that I typically add to
my `PATH` with various tools & utilities.

This was inspired by a number of talks at Polyglot 2013, as well as the
discussion at:

<http://stackoverflow.com/questions/17082038/efficient-way-to-manage-a-git-repository-for-local-config-files>

I used to have a script (`link_in_homedir.py`) that symlinked everything from this
repo to my actual home directory.  The thing I found though is that there's
always machine specific config that makes that difficult, and I'd end up just
copying stuff from my checked out copy of this repo to my home directory.  The
script is still around for inspiration, but is very much deprecated now.

## Structure

There are a handful of directories:

* `/dotfiles` - contains all hidden files that normally go in my root home
  directory (think things like `.bashrc`, `.gitconfig`, etc)
* `/bin` - a handful of various utilities & scripts to make life easier. I
  usually put this into my PATH.
* `/.git-templates` - some handy Git related hooks & such.
* `/.vscode` - some templates for tasks.json & settings files for
  [the best editor out there](https://code.visualstudio.com/)
* `/iterm` - I use [iTerm2](https://iterm2.com/) as my terminal of choice.
  Sometimes I export my settings for it to this directory

Most of these directories should be considered starting points for setting
stuff up.  Many of the files within them have to be tweaked to work for a
specific machine.

## Caveats/Issues/Notes

### Python Stuff

There's various Python utilities required for some of the scripts in bin.
Make sure you have a decent version of Python and pip installed.

### iTerm2

I use [iTerm2](http://www.iterm2.com/#/section/home) as my terminal of choice,
and my config can be found in `iterm/`

Having said that, I've largely given up on this as I've found that importing
settings from this folder often breaks in weird ways.  If someone has a good
way for exporting iTerm settings, please let me know.

In the meantime, I blogged about my iterm setup:
<https://www.codependentcodr.com/iterm2-setup.html#iterm2-setup>

## Other Setup Stuff

These are some other apps I install whenever I have to set up a new Mac.

### Homebrew

The best package manager: <https://brew.sh/>

### Git

Install via Homebrew as the version that comes with XCode is garbage:

```shell
brew install git
```

While at it, install git-extras:

```shell
brew install git-extras
```

### Pyenv

```shell
brew install pyenv
brew install pyenv-virtualenv
brew install pyenv-virtualenvwrapper
```

### Visual Studio Code

My editor of choice: <https://code.visualstudio.com/>

### Sublime Text

My 2nd editor of choice, LOL: <https://www.sublimetext.com/>

As well, I add the following keymappings:

```javascript
[
  { "keys": ["super+shift+k"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Delete Line.sublime-macro"} },
  { "keys": ["alt+up"], "command": "swap_line_up" },
  { "keys": ["alt+down"], "command": "swap_line_down" },
  { "keys": ["alt+shift+up"], "command": "duplicate_line" },
  { "keys": ["alt+shift+down"], "command": "duplicate_line" }
]
```

### Amphetamine

Amphetamine: <https://itunes.apple.com/ca/app/amphetamine/id937984704?mt=12>

### LolCat

```shell
sudo gem install lolcat
```

### Shpotify

Command line interface for controlling Spotify:

```shell
brew install shpotify
```

### ItsyCal

Itsycal: <https://www.mowglii.com/itsycal/>

### CPULed

<https://itunes.apple.com/ca/app/cpu-led/id448189857?mt=12>

### Spectacle

<http://spectacleapp.com/>

### Activity Timer

<https://apps.apple.com/us/app/activity-timer/id808647808>

### KeePassXC

<https://keepassxc.org/>

Though I have been using a very old version
([2.2.2](https://github.com/keepassxreboot/keepassxc/releases/tag/2.2.0))

### Pipx

```shell
brew install pipx
pipx ensurepath
```

### Misc Global Python Commands

All installed with Pipx.  Use the supplied `install_py_pkgs.sh` script.

```shell
./install_py_pkgs.sh
```

There's definitely other things I install, but that's a good start.

## Misc OSX Config Stuff

Maybe some of this could be automated/scripted?

### Show Hidden Files

Show hidden files, in terminal:

```shell
defaults write com.apple.Finder AppleShowAllFiles true
killall Finder
```

### Disable The Touchbar

Since it's horrible: <https://osxdaily.com/2018/08/30/disable-touch-bar-macbook-pro/>

## Other Examples of This

I'm not the first to throw my config/setup stuff into a source control repository,
others to look at for inspiration:

<https://bitbucket.org/j/dotfiles/src>

<https://github.com/garybernhardt/dotfiles>
