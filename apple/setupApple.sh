#!/bin/sh
set -e

# Inspired by:
# https://github.com/mathiasbynens/dotfiles/blob/master/.macos

echo "Setting misc OSX settings"

# ======================================================
# Misc OSX
# ======================================================

echo "-------------------"
echo "Finder settings...."
echo "- Show hidden files"
defaults write com.apple.Finder AppleShowAllFiles true

# for the hidden files everywhere:
# https://apple.stackexchange.com/questions/99213/is-it-possible-to-always-show-hidden-dotfiles-in-open-save-dialogs/99214#99214
defaults write -g AppleShowAllFiles -bool true
killall Finder
echo "Finder settings done"

echo "-------------------"
echo "Touchbar settings...."
echo "- set to f1 keys"
defaults write com.apple.touchbar.agent PresentationModeGlobal functionKeys
pkill "Touch Bar agent" || killall "ControlStrip" || true
echo "Touchbar settings done"

# Set Dock settings
echo "-------------------"
echo "Dock settings...."
echo "- setting icon size"
defaults write com.apple.dock tilesize 44
echo "- setting autohide on"
defaults write com.apple.dock autohide -bool true
echo "- setting orientation to bottom of screen"
defaults write com.apple.dock orientation bottom
echo "- setting top right hot corner to activate screen saver"
defaults write com.apple.dock wvous-tr-corner -int 5
defaults write com.apple.dock wvous-tr-modifier -int 0
echo "- setting magification"
defaults write com.apple.dock largesize 128
defaults write com.apple.dock magnification -bool true
echo "- setting don't rearrange spaces on most recent use"
defaults write com.apple.dock mru-spaces -bool false
killall Dock
echo "Dock settings done"

echo "-------------------"
echo "Display settings...."
echo "- displays have separate Spaces (requires log out)"
defaults write com.apple.spaces spans-displays -bool true
echo "Display settings done"

# ======================================================
# Spectacle
# ======================================================
echo "-------------------"
echo "Setting Spectacle settings...."
cp Spectacle/Shortcuts.json ~/Library/Application\ Support/Spectacle/Shortcuts.json
killall Spectacle
echo "Spectacle settings done (restart it to take effect)"
