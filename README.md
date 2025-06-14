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

This can be restored by following: <https://gitlab.com/gnachman/iterm2/-/issues/8029>

I've also blogged about my iterm setup:
<https://www.codependentcodr.com/iterm2-setup.html#iterm2-setup>

Also very important: make sure you install the shell integration:
<https://iterm2.com/documentation-shell-integration.html>

## Other Setup Stuff

These are some other apps I install whenever I have to set up a new Mac.

### Homebrew

The best package manager: <https://brew.sh/>

### Git

Install via `install_brew_pkgs.sh`

### asdf

Install via `install_brew_pkgs.sh`

### Visual Studio Code (VSCode)

My editor of choice: <https://code.visualstudio.com/>

Note that installing on a new machine, I had to reset the default shell, even
when using settings sync: <https://code.visualstudio.com/docs/terminal/profiles>

### Sublime Text

My 2nd editor of choice, LOL: <https://www.sublimetext.com/>

As well, I add the following keymappings (open "keybindings" in the command pallette):

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

### Rectangle

<https://rectangleapp.com/>

Settings are in `apple/Rectangle/RectangleConfig.json`

### Activity Timer

<https://apps.apple.com/us/app/activity-timer/id808647808>

### Horo

<https://matthewpalmer.net/horo-free-timer-mac/>

### Zappy

<https://zapier.com/zappy>

### InYourFace

<https://www.inyourface.app/>

### Stream Deck

<https://www.elgato.com/en/gaming/downloads>

There's also a couple plugins that have been pulled from the marketplace,
but are committed in the apple/streamdeck directory.  Unzip them to
`~/Library/Application\ Support/com.elgato.StreamDeck/Plugins`

I also have my config backed up elsewhere (mostly as there's a couple of
shortcuts that are sensitive to my work environment).

### Raycast

<https://www.raycast.com/>

I also have my config backed up elsewhere (mostly as there's a couple of
shortcuts & secrets that are sensitive to my work environment).

### Bartender

<https://macbartender.com/>

### KeePassXC

<https://keepassxc.org/>

### IstatMenus

<https://bjango.com/mac/istatmenus/>

### Pipx

Install via `install_brew_pkgs.sh`

### Starship

For that nice prompt goodness: <https://starship.rs/>

Install via `install_brew_pkgs.sh`

Then symlink (or copy) `.config/starship.toml` to `~/.config`.

I've also blogged about my Starship setup: <https://www.codependentcodr.com/using-starship-for-terminal-prompt-goodness.html>

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
defaults write -g AppleShowAllFiles -bool true

killall Finder
```

Source: <https://apple.stackexchange.com/questions/99213/is-it-possible-to-always-show-hidden-dotfiles-in-open-save-dialogs/99214#99214>

### Disable The Touchbar

Since it's horrible: <https://osxdaily.com/2018/08/30/disable-touch-bar-macbook-pro/>

## Other Examples of This

I'm not the first to throw my config/setup stuff into a source control repository,
others to look at for inspiration:

<https://bitbucket.org/j/dotfiles/src>

<https://github.com/garybernhardt/dotfiles>
